# coding=utf-8
"""
返回不同格式的约拍模型
@author：黄鑫晨
@attention: Model为模型，model为模特
"""
import time

from Database.models import get_db
from Database.tables import AppointLike, AppointmentImage, CompanionImg, User, AppointEntry, WApCompanionImage, \
    AppointmentInfo, UserImage
from FileHandler.AuthkeyHandler import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs


class APmodelHandler(object):

    @classmethod
    def ap_Model_simply(cls, appointments, retdata):
        """
        简单约拍模型，用于登录首页
        :param appointments: 传入多个appointment对象 
        :param retdata: 存储约拍信息
        :return:  返回多个简单约拍模型
        """
        # todo:查找待变更为最新10个

        try:
            for appointment in appointments:
                retdata.append(APmodelHandler.ap_Model_simply_one(appointment))
            return retdata
        except Exception, e:
            print e

    @classmethod
    def ap_get_imgs_by_apid(cls, appointment_id):
        """
        得到某约拍的图片
        Args:
            appointment_id: 约拍Id
        Returns:图片名数组
        """
        img_tokens = []
        authkey_handler = AuthKeyHandler()
        try:
            imgs = get_db().query(AppointmentImage).filter(AppointmentImage.APIapid == appointment_id).all()  # 返回所有图片项
            for img in imgs:
                img_url = img.APIurl
                img_tokens.append(authkey_handler.download_assign_url(img_url, 200, 200))
        except Exception,e:
            print '无图片'
        return img_tokens

    @classmethod
    def ap_Model_simply_one(cls, appointment):
        """
        得到简单约拍模型，约拍列表
        :param appointment: 传入一个appointment对象
        :return: 返回单个约拍简单模型
        """

        ap_imgurls = APmodelHandler.ap_get_imgs_by_apid(appointment.APid)
        headimage = Ufuncs.get_user_headimage_intent_from_userid(appointment.APsponsorid)
        user_id = appointment.APsponsorid     # 创建者的id
        user = get_db().query(User).filter(User.Uid == user_id).one()
        user_bir = user.Ubirthday.strftime('%Y')   # 获取用户生日（年）
        now = time.strftime('%Y', time.localtime(time.time()))  # 获取当前年份
        user_age = int(now)-int(user_bir) # 用户年龄
        user_sex = ("男" if user.Usex else "女")
        ret_ap = dict(
            APid=appointment.APid,
                # APtitle=appointment.APtitle,
                APimgurl=ap_imgurls,
                APtime=appointment.APtime,  # 这里我改过了。。。。 2017-4-7 兰威 apstartime
                APlikeN=appointment.APlikeN,
                APregistN=appointment.APregistN,
                Userimg=headimage,
                Userage=str(user_age)+"岁",
                Useralais=user.Ualais,
                APpricetype=appointment.APpricetag,
                APprice=appointment.APprice,
                Userlocation=user.Ulocation,
                APcreatetime=appointment.APcreateT.strftime("%Y-%m-%d %H:%M:%S"),
                Usex=user_sex,
                APcontent=appointment.APcontent,
                APgroup=appointment.APgroup,
                sponsorid=int(user_id),
                APstatus=appointment.APstatus
                )
        return ret_ap


    @classmethod
    def ap_Model_multiple(cls, appointment, userid):
        ap_regist_users = []
        registed = 0
        # liked = 0
        commented = 0

        try:
            headimage = Ufuncs.get_user_headimage_intent_from_userid(appointment.APsponsorid)
            apimgurls = APmodelHandler.ap_get_imgs_by_apid(appointment.APid)
            ap_regist_users = Ufuncs.get_userlist_from_ap(appointment.APid)
            user_id = appointment.APsponsorid  # 创建者的id
            user = get_db().query(User).filter(User.Uid == user_id).one()
            user_bir = user.Ubirthday.strftime('%Y')  # 获取用户生日（年）
            now = time.strftime('%Y', time.localtime(time.time()))  # 获取当前年份
            user_age = int(now) - int(user_bir)  # 用户年龄
            user_sex = ("男" if user.Usex else "女")
            exist = get_db().query(AppointEntry).filter(AppointEntry.AEregisterID
                                                        == userid, AppointEntry.AEapid == appointment.APid,\
                                                        AppointEntry.AEvalid == 1).all()
            if exist:
                registed = 1
            if appointment.APstatus == 3:
                appointmentinfo = get_db().query(AppointmentInfo).filter(
                    AppointmentInfo.AIappoid == appointment.APid).one()
                if int(userid) == appointmentinfo.AIpid:
                    if appointmentinfo.AIpcomment:
                        commented = 1
                if int(userid) == appointmentinfo.AImid:
                    if appointmentinfo.AImcomment:
                        commented = 1
            if appointment.APstatus == 4:
                commented = 1
            m_response = dict(
                APid=appointment.APid,
                # APtitle=appointment.APtitle,
                APsponsorid=appointment.APsponsorid,
                APtag=appointment.APtag,
                APtype=int(appointment.APtype),
                APlocation=appointment.APlocation,
                # APstartT=appointment.APstartT.strftime('%Y-%m-%d %H:%M:%S'),
                # APendT=appointment.APendT.strftime('%Y-%m-%d %H:%M:%S'),
                # APjoinT=appointment.APjoinT.strftime('%Y-%m-%d %H:%M:%S'),
                APtime=appointment.APtime,
                APcontent=appointment.APcontent,
                #APfree=int(appointment.APfree),
                APpricetag=appointment.APpricetag,
                APprice=appointment.APprice,
                APcreateT=appointment.APcreateT.strftime('%Y-%m-%d %H:%M:%S'),
                APaddallowed=int(appointment.APaddallowed),
                APlikeN=appointment.APlikeN,
                APvalid=int(appointment.APvalid),
                APregistN=appointment.APregistN,
                APregisters=ap_regist_users,  # 返回所有报名人用户模型
                APimgurl=apimgurls,
                APstatus=appointment.APstatus,
                #Userliked=liked,
                APgroup=appointment.APgroup,
                Userimg=headimage,
                Userage=str(user_age) + "岁",
                Useralais=user.Ualais,
                Userlocation=user.Ulocation,
                Usex=user_sex,
                Useregistd=registed,
                Usercommented=commented,
                sponsorid=int(user_id),
            )
            if appointment.APstatus == 4:  # 状态为4时返回两边的评价
                appointmentinfo = get_db().query(AppointmentInfo).filter(AppointmentInfo.AIappoid == appointment.APid).one()
                user_p_headimage = Ufuncs.get_user_headimage_intent_from_userid(appointmentinfo.AIpid)
                user_m_headimage = Ufuncs.get_user_headimage_intent_from_userid(appointmentinfo.AImid)
                user_p = get_db().query(User).filter(User.Uid == appointmentinfo.AIpid ).one()
                user_m = get_db().query(User).filter(User.Uid == appointmentinfo.AImid ).one()
                comment_p = dict(
                        uid=appointmentinfo.AIpid,
                        ucomment=appointmentinfo.AIpcomment,
                        uscore=appointmentinfo.AIpscore,
                        uheadimage=user_p_headimage,
                        ualias=user_p.Ualais
                )
                comment_m = dict(
                    uid = appointmentinfo.AImid,
                    ucomment=appointmentinfo.AImcomment,
                    uscore=appointmentinfo.AImscore,
                    uheadimage=user_m_headimage,
                    ualias=user_m.Ualais
                )
                comment = []
                comment.append(comment_p)
                comment.append(comment_m)
                m_response['comment'] = comment
            return m_response
        except Exception, e:
            print e, 'dff'


    @classmethod
    def ApInforesponse(appointment, retdata):
        '''
        Returns:返回选择约拍的人关于约拍的详细信息
        #todo:查找待变更为最新10个
        '''
        m_ApInforesponse = dict(
                AIid=appointment.AIid,
                AImid=appointment.AImid,
                AIpid=appointment.Aipid,
                AImscore=appointment.AImscore,
                AIpscore=appointment.AIpscore,
                AImcomment=appointment.AImcomment,
                AIpcomment=appointment.AIpcomment,
                AIappoid=appointment.AIappoid
        )
        retdata.append(m_ApInforesponse)


    def ApCompanion(clas, Companion, retdata):
        auth = AuthKeyHandler()
        Companion_imgs = get_db().query(WApCompanionImage).filter(WApCompanionImage.WAPCid == Companion.WAPCid).all()
        Imgs = []
        for item in Companion_imgs:
            Imgs.append(auth.download_url(item.WAPCurl))
        ApCompanion_model = dict(
            CompanionId=Companion.WAPCid,
            CompanionTitle=Companion.WAPCname,
            CompanionContent=Companion.WAPCServeintro,
            CompanionUrl=Companion.WAPCContact,
            CompanionPic=Imgs,
        )
        retdata.append(ApCompanion_model)




