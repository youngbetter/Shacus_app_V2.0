# coding=utf-8
"""
@author: hxc, covered by yh

"""
import json
from ctypes import cast

from sqlalchemy import desc
from sqlalchemy.sql.elements import or_


import Userinfo
from APmodel import APmodelHandler
from Appointment.APgroupHandler import APgroupHandler
from BaseHandler import BaseHandler
from Database.tables import Appointment, AppointEntry, User
from Userinfo import Ufuncs


class GetListHandler(BaseHandler):  # 请求约拍列表

    # todo:返回特定条件下的约拍
    retjson = {'code': '', 'contents': ''}

    def refresh_list(self, type, offset_apid, u_id):
        """
        :param type: 约拍发起者，模特发起0，摄影师发起1
        :param offset_apid:
        :param u_id: 用户id
        :return: 刷新出的约拍列表
        """
        retdata = []
        try:
            #  attention: <  因为返回新的
            appointments = self.db.query(Appointment). \
                filter(Appointment.APtype == type, Appointment.APclosed == 0, Appointment.APvalid == 1,
                       Appointment.APstatus == 0,
                       Appointment.APid < offset_apid).from_self().order_by(desc(Appointment.APcreateT)). \
                limit(6).all()      # 一次最多刷新出六个新的约拍
            if appointments:
                APmodelHandler.ap_Model_simply(appointments, retdata)
                self.retjson['code'] = '10253'  # 刷新成功，返回新约拍
                self.retjson['contents'] = retdata
            else:
                self.retjson['code'] = '10262'
                self.retjson['contents'] = r"没有更多约拍"

        except Exception, e:
            self.retjson['contents'] = '数据库错误'
            self.retjson['code'] = '10215'


    def no_result_found(self, e):
        print e
        self.retjson['code'] = '10261'
        self.retjson['contents'] = '未查询到约拍记录'

    def get_ap_Model_by_aeids(self, appoint_entries):    # 通过约拍条目表获取约拍
        ap_ids = []
        for ap_entry in appoint_entries:
            ap_id = ap_entry.AEapid
            ap_ids.append(ap_id)
        return self.get_ap_Model_by_apids(ap_ids)      # 通过约拍表获取约拍

    def get_ap_Model_by_apids(self, apids):
        appointments = []
        for apid in apids:
            appointment = self.db.query(Appointment).filter(Appointment.APid == apid).one()
            appointments.append(appointment)
        return appointments

    def ap_ask_user(self, uid, retdata):  # 查询指定用户的所有约拍
        """
        :param uid: 传入一个User对象
        :return: 无返回，直接修改retjson
        """
        # 判断该用户是否存在
        try:
            user = self.db.query(User).filter(User.Uid == uid).one()
            if user:
                pass
            else:
                self.retjson['code'] = '100001'
                self.retjson['contents'] = "查询的用户不存在"
                return
        except Exception, e:
            self.retjson['contents'] = '数据库错误'
            self.retjson['code'] = '10215'

        try:
            appointments1 = self.db.query(Appointment).filter(Appointment.APsponsorid == uid,\
                                                              Appointment.APvalid == 1).all()  # 用户自己发起的
            appointentries = self.db.query(AppointEntry).filter(AppointEntry.AEregisterID == uid,\
                                                               AppointEntry.AEvalid == 1).all()  # 用户报名的

            APmodelHandler.ap_Model_simply(appointments1, retdata)
            APmodelHandler.ap_Model_simply(self.get_ap_Model_by_aeids(appointentries), retdata)
            self.retjson['code'] = '10256'
            self.retjson['contents'] = retdata
        except Exception, e:
            print e
            self.no_result_found(e)

    def refresh_group_list(self, type, offset_apid, u_id, group):
        retdata = []
        if int(group) != 0:
            try:
                # attention: 因为返回新的
                appointments = self.db.query(Appointment). \
                    filter(Appointment.APtype == type, Appointment.APclosed == 0, Appointment.APvalid == 1,
                           Appointment.APstatus == 0,or_(Appointment.APgroup.like("{}%".format(group)),\
                                                         Appointment.APgroup.like("%{}".format(group))),
                           Appointment.APid < offset_apid).from_self().order_by(desc(Appointment.APcreateT)). \
                    limit(6).all()
                if appointments:
                    APmodelHandler.ap_Model_simply( appointments, retdata)
                    self.retjson['code'] = '10253'  # 刷新成功
                    self.retjson['contents'] = retdata

                else:
                    self.retjson['code'] = '10262'
                    self.retjson['contents'] = r"没有更多约拍"

            except Exception, e:
                self.retjson['contents'] = '数据库错误'
                self.retjson['code'] = '10215'
        else:
            self.refresh_list(type, offset_apid, u_id)

    def post(self):

        request_type = self.get_argument('type')
        u_auth_key = self.get_argument('authkey')
        u_id = self.get_argument('uid')
        ufuncs = Userinfo.Ufuncs.Ufuncs()
        retdata = []

        if ufuncs.judge_user_valid(u_id, u_auth_key):

            if request_type == '10231':  # 请求所有设定地点的摄影师发布的约拍中未关闭的
                ap_group = self.get_argument('group')
                try:
                    if int(ap_group) == 0:
                        appointments = self.db.query(Appointment). \
                            filter(Appointment.APtype == 1, Appointment.APclosed == 0, Appointment.APvalid == 1,
                                   Appointment.APstatus == 0).\
                            order_by(desc(Appointment.APid)).limit(6).all()
                        APmodelHandler.ap_Model_simply(appointments, retdata)
                        self.retjson['code'] = '10251'
                        self.retjson['contents'] = retdata
                    else:
                        appointments = self.db.query(Appointment). \
                            filter(Appointment.APtype == 1, Appointment.APclosed == 0, Appointment.APvalid == 1,
                                   Appointment.APstatus == 0, or_(Appointment.APgroup.like("{}%".format(ap_group)),Appointment.APgroup.like("%{}".format(ap_group)))). \
                            order_by(desc(Appointment.APid)).limit(6).all()
                        APmodelHandler.ap_Model_simply(appointments, retdata)
                        self.retjson['code'] = '10251'
                        self.retjson['contents'] = retdata
                except Exception, e:  # 没有找到约拍
                    print e
                    self.no_result_found(e)
            elif request_type == '10235':  # 请求所有设定地点的模特发布的约拍中未关闭的
                ap_group = self.get_argument('group')
                try:

                    if int(ap_group) == 0:
                            appointments = self.db.query(Appointment). \
                                filter(Appointment.APtype == 0, Appointment.APclosed == 0, Appointment.APvalid == 1,
                                       Appointment.APstatus == 0,).\
                            order_by(desc(Appointment.APid)).limit(6).all()
                            APmodelHandler.ap_Model_simply(appointments, retdata)
                            self.retjson['code'] = '10252'
                            self.retjson['contents'] = retdata
                    else:
                        appointments = self.db.query(Appointment). \
                            filter(Appointment.APtype == 0, Appointment.APclosed == 0, Appointment.APvalid == 1,
                                   Appointment.APstatus == 0, or_(Appointment.APgroup.like("{}%".format(ap_group)),Appointment.APgroup.like("%{}".format(ap_group)))). \
                            order_by(desc(Appointment.APid)).limit(6).all()
                        APmodelHandler.ap_Model_simply(appointments, retdata)
                        self.retjson['code'] = '10252'
                        self.retjson['contents'] = retdata
                except Exception, e:
                    self.no_result_found(e)

            elif request_type == '10240':  # 请求自己参与（包括发布）的所有约拍
                self.ap_ask_user(u_id, retdata)

            elif request_type == '10241':  # 请求指定用户参与的所有约拍
                find_u_id = self.get_argument('finduid')
                self.ap_ask_user(find_u_id, retdata)

            elif request_type == '10243':  # 刷新并拿到指定Id后的6个摄影师约拍
                ap_group = self.get_argument('group')
                offset_apid = self.get_argument('offsetapid')
                self.refresh_group_list(1, offset_apid, u_id,ap_group)

            elif request_type == '10244':  # 刷新并拿到指定Id后的6个模特约拍
                ap_group = self.get_argument('group')
                offset_apid = self.get_argument('offsetapid')
                self.refresh_group_list(0, offset_apid,  u_id, ap_group)

            elif request_type == '10245':  # 返回报名某约拍的全部用户列表
                ap_id = self.get_argument('apid')
                try:
                    # todo：利用join
                    appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id).one()  # 查找是否有此约拍
                    if appointment:
                        try:
                            user_ids = Ufuncs.Ufuncs.get_registids_from_appointment(appointment)
                            registers = Ufuncs.Ufuncs.get_users_chooselist_from_uids(user_ids, appointment.APid)
                            self.retjson['code'] = '10257'
                            self.retjson['contents'] = registers
                        except Exception, e:
                            print e
                            self.retjson['code'] = '10257'
                            self.retjson['contents'] = u'读写错误'

                except Exception, e:
                    print e
                    self.retjson['code'] = '10264'
                    self.retjson['contents'] = u'未查询到报名人'

        else:
            self.retjson['contents'] = '授权码不存在或已过期'
            self.retjson['code'] = '10214'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

