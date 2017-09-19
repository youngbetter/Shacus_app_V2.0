# coding=utf-8
"""
选择约拍对象，只能选一个
"""

import json

from BaseHandler import BaseHandler
from Userinfo import Ufuncs
from Database.tables import ActivityEntry, Activity, AppointEntry, Appointment, AppointmentInfo, ActivityImage


class ChooseOneHandler(BaseHandler):

    retjson = {"code": '', 'contents': ''}

    def post(self):
        type = self.get_argument('type')
        u_id = self.get_argument('uid')
        auth_key = self.get_argument('authkey')
        ufuncs = Ufuncs.Ufuncs()

        if ufuncs.judge_user_valid(u_id, auth_key):
            if type == '10904':   # 选择约拍对象
                apid = self.get_argument('apid')
                chooseuid = self.get_argument('chooseduid')
                try:
                    regist_entry = self.db.query(AppointEntry). \
                        filter(AppointEntry.AEregisterID == chooseuid, AppointEntry.AEapid == apid).one()  # 查找报名项
                    if regist_entry:
                        if regist_entry.AEvalid == 1:    # 用户未取消报名
                            if regist_entry.AEchoosed:
                                self.retjson['contents'] = u'之前已选择过该用户！'
                            else:  # 用户报名中且未被选择，添加新的约拍项
                                regist_entry.AEchoosed = 1  # 该用户被选择
                                try:
                                    appointment = self.db.query(Appointment.APid, Appointment.APsponsorid, \
                                                                Appointment.APtype, Appointment.APstatus). \
                                        filter(Appointment.APid == regist_entry.AEapid,\
                                               Appointment.APvalid == 1, Appointment.APstatus == 0).one()
                                    if appointment.APsponsorid == int(u_id):    # 该操作用户是发起者
                                        mid = pid = 0
                                        if appointment.APtype == 1:  # 发起者是摄影师：
                                            mid = chooseuid
                                            pid = u_id
                                        elif appointment.APtype == 0:  # 发起者是模特：
                                            mid = u_id
                                            pid = chooseuid
                                        print 'before change'
                                        self.db.query(Appointment).filter(Appointment.APid == appointment.APid). \
                                            update({"APstatus": 1}, synchronize_session='evaluate')  # 将该约拍项移到进行中
                                        print 'after change'
                                        new_appinfo = AppointmentInfo(
                                            AImid=mid,
                                            AIpid=pid,
                                            AIappoid=apid
                                        )
                                        try:
                                            self.db.merge(new_appinfo)
                                            self.db.commit()
                                            self.retjson['code'] = '10920'
                                            self.retjson['contents'] = u"选择约拍对象成功"
                                        except Exception, e:
                                            print e
                                            self.retjson['code'] = '10925'
                                            self.retjson['contents'] = u"数据库插入错误"
                                    else:
                                        self.retjson['code'] = '10921'
                                        self.retjson['contents'] = u"该用户没有选择权限！"
                                except Exception, e:
                                    print e
                                    self.retjson['code'] = '10924'
                                    self.retjson['contents'] = u'该约拍不存在或已过期'
                        else:
                            self.retjson['code'] = '10923'
                            self.retjson['contents'] = u'用户已取消报名！'
                except Exception, e:
                    print e
                    self.retjson['code'] = '10922'
                    self.retjson['contents'] = u'选择用户未报名该约拍'

            elif type == '10905':     # 完成约拍
                apid = self.get_argument('apid')
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == apid).one()
                    app_entry = self.db.query(AppointEntry).filter(AppointEntry.AEapid == apid,\
                                                                   AppointEntry.AEchoosed == 1).one()
                    if appointment.APsponsorid == int(u_id):      # 确认权限，是约拍发起者
                        if appointment.APstatus == 1:        # 确认约拍状态
                            print 2
                            try:
                                app_info = self.db.query(AppointmentInfo).filter(AppointmentInfo.AIappoid == apid).one()
                                if appointment.APtype == 1:  # 发起者是摄影师：
                                    if app_info.AIpfinish == 1:
                                        self.retjson['code'] = '109052'
                                        self.retjson['contents'] = u'您已确认过，请勿重复确认'
                                    else:
                                        app_info.AIpfinish = 1
                                        if app_info.AImfinish == 1:
                                            appointment.APstatus = 2
                                            try:
                                                self.db.commit()
                                                self.retjson['code'] = '109050'
                                                self.retjson['contents'] = u'双方确认成功'
                                            except Exception, e:
                                                print e
                                                self.retjson['code'] = '109056'
                                                self.retjson['contents'] = u'数据库修改错误'
                                        else:
                                            try:
                                                self.db.commit()
                                                self.retjson['code'] = '109051'
                                                self.retjson['contents'] = u'确认成功,等待对方确认'
                                            except Exception, e:
                                                print e
                                                self.retjson['code'] = '109056'
                                                self.retjson['contents'] = u'数据库修改错误'

                                elif appointment.APtype == 0:  # 发起者是模特：
                                    if app_info.AImfinish == 1:
                                        self.retjson['code'] = '109052'
                                        self.retjson['contents'] = u'您已确认过，请勿重复确认'
                                    else:
                                        app_info.AImfinish = 1
                                        if app_info.AIpfinish == 1:
                                            appointment.APstatus = 2
                                            try:
                                                self.db.commit()
                                                self.retjson['code'] = '109050'
                                                self.retjson['contents'] = u'双方确认成功'
                                            except Exception, e:
                                                print e
                                                self.retjson['code'] = '109056'
                                                self.retjson['contents'] = u'数据库修改错误'
                                        else:
                                            try:
                                                self.db.commit()
                                                self.retjson['code'] = '109051'
                                                self.retjson['contents'] = u'确认成功,等待对方确认'
                                            except Exception, e:
                                                print e
                                                self.retjson['code'] = '109056'
                                                self.retjson['contents'] = u'数据库修改错误'
                            except Exception, e:
                                print e
                                self.retjson['code'] = '109053'
                                self.retjson['contents'] = u'该约拍信息不存在'
                        else:
                            self.retjson['code'] = '109054'
                            self.retjson['contents'] = u'确认失败，请确认约拍状态'

                    elif app_entry.AEregisterID == int(u_id):    # 报名用户确认完成
                        print 'i am register'
                        if appointment.APstatus == 1:        # 确认约拍状态
                            print 3
                            try:
                                app_info = self.db.query(AppointmentInfo).filter(AppointmentInfo.AIappoid == apid).one()
                                #app = self.db.query(Appointment).filter(Appointment.APid == apid).one()
                                if appointment.APtype == 1:  # 发起者是摄影师：
                                    if app_info.AImfinish == 1:
                                        self.retjson['code'] = '109052'
                                        self.retjson['contents'] = u'您已确认过，请勿重复确认'
                                    else:
                                        app_info.AImfinish = 1
                                        if app_info.AIpfinish == 1:
                                            appointment.APstatus = 2
                                            try:
                                                self.db.commit()
                                                self.retjson['code'] = '109050'
                                                self.retjson['contents'] = u'双方确认成功'
                                            except Exception, e:
                                                print e
                                                self.retjson['code'] = '109056'
                                                self.retjson['contents'] = u'数据库修改错误'
                                        else:
                                            try:
                                                self.db.commit()
                                                self.retjson['code'] = '109051'
                                                self.retjson['contents'] = u'确认成功,等待对方确认'
                                            except Exception, e:
                                                print e
                                                self.retjson['code'] = '109056'
                                                self.retjson['contents'] = u'数据库修改错误'

                                elif appointment.APtype == 0:  # 发起者是模特：
                                    if app_info.AIpfinish == 1:
                                        self.retjson['code'] = '109052'
                                        self.retjson['contents'] = u'您已确认过，请勿重复确认'
                                    else:
                                        app_info.AIpfinish = 1
                                        if app_info.AImfinish == 1:
                                            appointment.APstatus = 2
                                            try:
                                                self.db.commit()
                                                self.retjson['code'] = '109050'
                                                self.retjson['contents'] = u'双方确认成功'
                                            except Exception, e:
                                                print e
                                                self.retjson['code'] = '109056'
                                                self.retjson['contents'] = u'数据库修改错误'
                                        else:
                                            try:
                                                self.db.commit()
                                                self.retjson['code'] = '109051'
                                                self.retjson['contents'] = u'确认成功,等待对方确认'
                                            except Exception, e:
                                                print e
                                                self.retjson['code'] = '109056'
                                                self.retjson['contents'] = u'数据库修改错误'
                            except Exception, e:
                                print e
                                self.retjson['code'] = '109053'
                                self.retjson['contents'] = u'该约拍信息不存在'
                        else:
                            self.retjson['code'] = '109054'
                            self.retjson['contents'] = u'确认失败，请确认约拍状态'

                except Exception, e:
                    print e
                    self.retjson['code'] = '109055'
                    self.retjson['contents'] = u'未查到该约拍信息'

        else:
            self.retjson['code'] = '10391'
            self.retjson['contents'] = '用户认证失败'

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
