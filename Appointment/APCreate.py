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

        ap_type = self.get_argument('type')
        u_auth_key = self.get_argument('authkey')
        u_id = self.get_argument('uid')
        ufuncs = Ufuncs.Ufuncs()

        if ufuncs.judge_user_valid(u_id, u_auth_key):

            if ap_type == '80000' or ap_type == '80001':  # 请求创建约拍
                ap_content = self.get_argument('contents')
                ap_imgs = self.get_argument('imgs')

                retjson_body = {'auth_key': '', 'apId': ''}
                auth_key_handler = AuthKeyHandler()
                ap_imgs_json = json.loads(ap_imgs)
                retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)
                if ap_type == '80000':  # 摄影师约模特
                    type_ap = 1
                elif ap_type == '80001':  # 模特约摄影师
                    type_ap = 0

                new_appointment = Appointment(

                    APsponsorid=u_id,
                    APtype=type_ap,
                    APlocation='',
                    APtime='0000-00-00:00:00:00',
                    APcontent=ap_content,  # 活动介绍
                    APclosed=0,
                    APvalid=1,
                    APaddallowed=0
                )
                try:
                    self.db.merge(new_appointment)
                    self.db.commit()
                    print '插入成功，进入查询'
                    ap = self.db.query(Appointment).filter(Appointment.APcontent == ap_content).order_by(
                        desc(Appointment.APcreateT)).all()
                    ap_id = ap[0].APid
                    retjson_body['apId'] = ap_id
                    self.retjson['code'] = '800001'  # 发布成功
                    self.retjson['contents'] = retjson_body

                except Exception, e:
                    print '插入失败！！'
                    self.retjson['code'] = '800002'
                    self.retjson['contents'] = r'服务器插入失败'

            elif ap_type == '80002':    # 取消约拍
                ap_id = self.get_argument('apid')
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id, \
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






