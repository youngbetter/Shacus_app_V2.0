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
                                        filter(Appointment.APid == regist_entry.AEapid).one()
                                    if appointment.APsponsorid == int(u_id):  # 该操作用户是发起者
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
                                        newappinfo = AppointmentInfo(
                                            AImid=mid,
                                            AIpid=pid,
                                            AIappoid=apid
                                        )
                                        try:
                                            self.db.merge(newappinfo)
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
                    self.retjson['contents'] = u'选择用户未报名该约拍'

        else:
            self.retjson['code'] = '10391'
            self.retjson['contents'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
