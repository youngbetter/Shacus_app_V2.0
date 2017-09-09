# coding=utf-8
import json

from BaseHandler import BaseHandler
from Database.tables import User, AppointEntry, Appointment
from Userinfo.Ufuncs import Ufuncs

'''
@author: wjl, hxc, modified by ye
'''


class APRegistHandler(BaseHandler):   # 报名约拍

    retjson = {'code': '', 'contents': ''}

    def db_error(self):
        self.db.rollback()
        self.retjson['contents'] = '数据库修改错误'
        self.retjson['code'] = '800032'

    def post(self):
        ap_type = self.get_argument('type')
        u_id = self.get_argument('uid')
        u_auth_key = self.get_argument('authkey')
        ap_id = self.get_argument('apid')
        ufunc = Ufuncs()

        if ufunc.judge_user_valid(u_id, u_auth_key):  # 用户认证成功
            if ap_type == '80003':   # 报名约拍
                # ap_message = self.get_argument('message')
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id).one()
                    if appointment.APvalid == 0:
                        self.retjson['contents'] = '该约拍已删除'
                        self.retjson['code'] = '800035'
                    else:
                        if appointment.APstatus == 0:    # 还在报名期
                            try:
                                exist = self.db.query(AppointEntry). \
                                    filter(AppointEntry.AEregisterID == u_id, AppointEntry.AEapid == ap_id,
                                           ).one()

                                if exist.AEvalid == 1:
                                    self.retjson['contents'] = '已报名过该约拍'
                                    self.retjson['code'] = '800030'
                                else:
                                    try:
                                        exist.AEvalid = 1
                                        appointment.APregistN += 1
                                        self.db.commit()
                                        self.retjson['contents'] = '报名成功'
                                        self.retjson['code'] = '800031'
                                    except Exception, e:
                                        self.db_error()
                            except Exception, e:
                                print e
                                new_appointment_entry = AppointEntry(
                                    AEapid=ap_id,
                                    AEregisterID=u_id,
                                    AEvalid=1,
                                    AEchoosed=0,
                                    # AEmessage=ap_message,
                                )
                                try:
                                    self.db.merge(new_appointment_entry)
                                    appointment.APregistN += 1
                                    self.db.commit()
                                    self.retjson['contents'] = '报名成功'
                                    self.retjson['code'] = '800031'
                                except Exception, e:
                                    print e
                                    self.db_error()
                        else:
                             self.retjson['contents'] = '该约拍报名期已过'
                             self.retjson['code'] = '800036'
                except Exception, e:
                    print e
                    self.retjson['contents'] = '数据库查询失败'
                    self.retjson['code'] = '800033'

            elif ap_type == '80004':   # 用户取消报名
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id).one()
                    if appointment.APvalid == 0:
                        self.retjson['contents'] = '该约拍已删除'
                        self.retjson['code'] = '800035'
                    else:
                        if appointment.APstatus == 0:
                            try:
                                entry = self.db.query(AppointEntry).filter(AppointEntry.AEapid == ap_id,\
                                                                           AppointEntry.AEregisterID == u_id).one()
                                if entry.AEvalid == 0:
                                    self.retjson['contents'] = '该约拍已取消'
                                    self.retjson['code'] = '800037'

                                else:
                                    try:
                                        entry.AEvalid = 0
                                        appointment.APregistN -= 1
                                        self.db.commit()
                                        self.retjson['contents'] = '取消约拍成功'
                                        self.retjson['code'] = '800038'

                                    except Exception, e:
                                        self.db_error()
                            except Exception, e:
                                print e
                                self.retjson['contents'] = '数据库查询失败'
                                self.retjson['code'] = '800033'
                        else:
                             self.retjson['contents'] = '该约拍已过报名期，不能取消'
                             self.retjson['code'] = '800039'
                except Exception, e:
                    print e
                    self.retjson['contents'] = '数据库查询出错'
                    self.retjson['code'] = '800034'

        else:
            self.retjson['code'] = '10272'
            self.retjson['contents'] = r'用户认证失败'
     
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
