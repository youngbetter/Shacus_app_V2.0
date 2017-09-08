# -*- coding: utf-8 -*-

import random
import json
from BaseHandler import BaseHandler

from Database.tables import User, UCinfo, Image, UserImage, Appointment, UserLike, UserCollection
from Database.tables import Verification
from message import message


def generate_verification_code(len=6):
    """随机生成6位的验证码"""
    code_list = []
    for i in range(10):
        code_list.append(str(i))
    myslice = random.sample(code_list, len)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)  # list to string
    return verification_code


def generate_auth_key(len=32):
    # 随机生成32位的验证码
    code_list = []
    for i in range(10):
        code_list.append(str(i))
    for i in range(65, 91):
        code_list.append(chr(i))
    for i in range(97, 123):
        code_list.append(chr(i))
    myslice = random.sample(code_list, len)
    auth_key = ''.join(myslice)
    return auth_key


class RegisterHandler(BaseHandler):
    print '进入register'
    retjson = {'code':'400','contents':'None'}

    def post(self):
        type = self.get_argument('type', default='unsolved')
        if type == '10001':   # 验证手机号
            m_phone = self.get_argument('phone')
            try:
                user = self.db.query(User).filter(User.Utel == m_phone).one()
                if user:
                    self.retjson['contents'] = u"该手机号已经被注册，请更换手机号或直接登录"
                    self.retjson['code'] = "10005"
            except:
                code = generate_verification_code()
                veri = Verification(
                    Vphone=m_phone,
                    Vcode=code,
                )
                self.db.merge(veri)
                try:
                    self.db.commit()
                    self.retjson['code'] = '10004'  # success
                    self.retjson['contents'] = u'手机号验证成功，发送验证码'
                except:
                    self.db.rollback()
                    self.retjson['code'] = '10009'  # Request Timeout
                    self.retjson['contents'] = u'服务器错误'
                message(code, m_phone)

        elif type == '10002':   # 验证验证码
            m_phone = self.get_argument('phone')
            code = self.get_argument('code')
            try:
                item = self.db.query(Verification).filter(Verification.Vphone == m_phone).one()
                # exist = self.db.query(Verification).filter(Verification.Vphone == m_phone).one()
                # delta = datetime.datetime.now() - exist.VT
                if item.Vcode == code:
                    # if delta>datetime.timedelta(minutes=10):
                    self.retjson['code'] = '10004'
                    self.retjson['contents'] = u'验证码验证成功'
                else:
                    self.retjson['code'] = '10006'
                    self.retjson['contents'] = u'验证码验证失败'
            except:
                self.retjson['code'] = '10007'
                self.retjson['contents'] = u'该手机号码未发送验证码'

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
