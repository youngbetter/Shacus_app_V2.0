# coding=utf-8
"""
 @author:hxc, covered by ye
 2017.9.8
"""

import json

from sqlalchemy import desc

from Appointment.APgroupHandler import APgroupHandler
from BaseHandler import BaseHandler
from Database.tables import Appointment, User
from FileHandler.ImageHandler import ImageHandler
from FileHandler.Upload import AuthKeyHandler
from Userinfo import Ufuncs


class APCreateHandler(BaseHandler):   # 创建约拍

    retjson = {'code': '', 'contents': 'None'}

    def post(self):

        type = self.get_argument('type')
        u_auth_key = self.get_argument('authkey')
        u_id = self.get_argument('uid')
        ufuncs = Ufuncs.Ufuncs()

        if ufuncs.judge_user_valid(u_id, u_auth_key):

            if type == '80000':  # 请求创建约拍第一步，获取图片上传凭证
                ap_imgs = self.get_argument('imgs')

                retjson_body = {}
                auth_key_handler = AuthKeyHandler()
                ap_imgs_json = json.loads(ap_imgs)
                retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)
                self.retjson['code'] = '800003'
                self.retjson['contents'] = retjson_body

            elif type == '80001':     # 请求创建约拍第二步，正式创建
                ap_type = self.get_argument('ap_type')
                ap_group = self.get_argument("group")
                ap_time_request = self.get_argument("time")
                price_type = self.get_argument("priceType")
                ap_price = self.get_argument('price')
                ap_content = self.get_argument('contents')
                ap_imgs = self.get_argument('imgs')
                new_appointment = Appointment(

                    APsponsorid=u_id,
                    APtype=int(ap_type),
                    APgroup=ap_group,
                    APpricetag=int(price_type),
                    APprice=ap_price,
                    APlocation='',
                    APtime=ap_time_request,
                    APcontent=ap_content,  # 活动介绍
                    APclosed=0,
                    APvalid=1,
                    APaddallowed=0
                )
                ap_imgs_json = json.loads(ap_imgs)
                imghandler = ImageHandler()
                try:
                    self.db.merge(new_appointment)
                    self.db.commit()
                    if ap_imgs_json:
                        ap = self.db.query(Appointment).filter(Appointment.APcontent == ap_content).order_by(
                            desc(Appointment.APcreateT)).all()
                        ap_id = ap[0].APid
                        imghandler.insert_appointment_image(ap_imgs_json, ap_id)
                    self.retjson['code'] = '800001'  # 发布成功
                    self.retjson['contents'] = '发布约拍成功'

                except Exception, e:
                    print '插入失败！！'
                    self.retjson['code'] = '800002'
                    self.retjson['contents'] = r'约拍发布失败'

            elif type == '80002':    # 取消约拍
                ap_id = self.get_argument('apid')
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id,\
                                                                    Appointment.APsponsorid == u_id).one()
                    if appointment.APvalid == 1:     # 约拍有效
                        if appointment.APstatus == 0:    # 还在报名中
                            appointment.APvalid = 0
                            try:
                                self.db.commit()
                                self.retjson['code'] = '800004'
                                self.retjson['contents'] = '成功取消约拍！'
                            except Exception, e:
                                print '修改失败！！'
                                self.retjson['code'] = '800005'
                                self.retjson['contents'] = r'取消约拍失败'
                        else:
                            self.retjson['code'] = '800006'
                            self.retjson['contents'] = r'约拍正在进行或已完成,不能取消'
                    else:
                        self.retjson['code'] = '800007'
                        self.retjson['contents'] = r'该约拍之前已被取消'
                except Exception, e:
                    self.retjson['code'] = '800008'
                    self.retjson['contents'] = '未发布该约拍！'

        else:
            self.retjson['contents'] = '授权码不存在或已过期'
            self.retjson['code'] = '800009'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))






