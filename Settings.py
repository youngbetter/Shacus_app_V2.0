# -*- coding:utf-8 -*-
'''
@author：yh
'''
import json

from BaseHandler import BaseHandler
from Database.tables import User
from FileHandler.Upload import AuthKeyHandler
from Userinfo import Ufuncs
from FileHandler.ImageHandler import ImageHandler


class PswChange(BaseHandler):

    retjson = {'code': '200','contents': 'none'}
    retdata = []

    def post(self):
        type = self.get_argument("type", default="null")
        if type == '10501':
            user_id = self.get_argument("user_id", "none")
            p_password = self.get_argument("old_psw")
            data = self.db.query(User).filter(user_id == User.Uid).one()
            if data.Upassword == p_password:
                self.retjson['code'] = '10501'
                self.retjson['contents'] = '获得修改密码权限'
            else:
                self.retjson['code'] = '10502'
                self.retjson['contents'] = '没有获得修改密码权限'
                
        elif type == '10511':
            user_id = self.get_argument("user_id", "none")
            m_password = self.get_argument("new_psw")
            try:
                data = self.db.query(User).filter(user_id == User.Uid).one()
                data.Upassword = m_password
                self.db.commit()
                self.retjson['code'] = '10511'
                self.retjson['contents'] = '修改密码成功'
            except Exception, e:
                print e
                self.retjson['code'] = '10512'
                self.retjson['contents'] = '修改密码失败'
                
        elif type == '10503':  # 修改用户昵称
                user_id = self.get_argument("user_id", "none")
                user_nickname = self.get_argument("user_nickname", "none")
                try:
                    data = self.db.query(User).filter(user_id == User.Uid).one()
                    data.Ualais = user_nickname
                    self.db.commit()
                    self.retjson['code'] = '10503'
                    self.retjson['contents'] = '修改昵称成功'
                except Exception, e:
                    print e
                    self.retjson['code'] = '10504'
                    self.retjson['contents'] = '修改昵称失败'

        elif type == '10505':  # 修改手机号
            user_id = self.get_argument("user_id", "none")
            user_phone = self.get_argument("user_phone", "none")
            try:
                data = self.db.query(User).filter(user_id == User.Uid).one()
                data.Utel = user_phone
                self.db.commit()
                self.retjson['code'] = '10505'
                self.retjson['contents'] = '修改绑定手机号成功'
            except Exception, e:
                print e
                self.retjson['code'] = '10506'
                self.retjson['contents'] = '修改绑定手机号失败'

        elif type == '10507':  # 修改地址
            user_id = self.get_argument("user_id", "none")
            user_location = self.get_argument("user_location", "none")
            try:
                data = self.db.query(User).filter(user_id == User.Uid).one()
                data.Ulocation = user_location
                self.db.commit()
                self.retjson['code'] = '10507'
                self.retjson['contents'] = '修改所在地成功'
            except Exception, e:
                print e
                self.retjson['code'] = '10508'
                self.retjson['contents'] = '修改所在地失败'

        elif type == '10509':  # 修改邮箱
            user_id = self.get_argument("user_id", "none")
            user_mail = self.get_argument("user_mail", "none")
            try:
                data = self.db.query(User).filter(user_id == User.Uid).one()
                data.Umailbox = user_mail
                self.db.commit()
                self.retjson['code'] = '10509'
                self.retjson['contents'] = '修改邮箱成功'
            except Exception, e:
                print e
                self.retjson['code'] = '10510'
                self.retjson['contents'] = '修改邮箱失败'

        # 修改头像，第一次存储图片，返回token
        elif type == '10513':

            # todo:第一二次握手之间应该加一个验证码

            u_id = self.get_argument('uid')
            u_authkey = self.get_argument('authkey')
            image = self.get_argument('image')
            ufuncs = Ufuncs.Ufuncs()
            if ufuncs.judge_user_valid(u_id, u_authkey):
                retjson_body = {'image_token': ''}
                image_token_handler = AuthKeyHandler()
                m_image_json = json.loads(image)
                self.retjson['contents'] = image_token_handler.generateToken(m_image_json)
                self.retjson['code'] = '10515'
            else :
                self.retjson['contents'] = '用户授权码不正确'
                self.retjson['code'] = '10514'
        elif type == '10516':
            u_id = self.get_argument('uid')
            u_authkey = self.get_argument('authkey')
            image = self.get_argument('image')
            ufuncs = Ufuncs.Ufuncs()
            if ufuncs.judge_user_valid(u_id, u_authkey):
                m_image_json = json.loads(image)
                auth = AuthKeyHandler()
                im = ImageHandler()
                im.change_user_headimage(m_image_json,u_id)
                self.retjson['contents'] = auth.download_assign_url(m_image_json[0], 200, 200)
                self.retjson['code'] = '66666'
            else:
                self.retjson['contents'] = '用户授权码不正确'
                self.retjson['code'] = '10514'

        elif type == '10517':  # 修改签名
            u_id = self.get_argument('uid')
            u_authkey = self.get_argument('authkey')
            sign = self.get_argument('sign')
            ufuncs = Ufuncs.Ufuncs()
            if ufuncs.judge_user_valid(u_id, u_authkey):
                user = self.db.query(User).filter(User.Uid == u_id).one()
                user.Usign = sign
                self.db.commit()
                self.retjson['contents'] = '修改个性签名成功'
                self.retjson['code'] = '10518'
            else:
                self.retjson['contents'] = '用户授权码不正确'
                self.retjson['code'] = '10514'

        elif type == '10519':  # 修改性别
            u_id = self.get_argument('uid')
            u_authkey = self.get_argument('authkey')
            gender = self.get_argument('gender')
            ufuncs = Ufuncs.Ufuncs()
            if ufuncs.judge_user_valid(u_id, u_authkey):
                user = self.db.query(User).filter(User.Uid == u_id).one()
                if gender == '1':
                    user.Usex = True
                else:
                    user.Usex = False
                self.db.commit()
                self.retjson['contents'] = '修改性别成功'
                self.retjson['code'] = '10519'
            else:
                self.retjson['contents'] = '用户授权码不正确'
                self.retjson['code'] = '10514'

        elif type == '10521':  # 修改生日
            u_id = self.get_argument('uid')
            u_authkey = self.get_argument('authkey')
            birthday = self.get_argument('birthday')
            ufuncs = Ufuncs.Ufuncs()
            if ufuncs.judge_user_valid(u_id, u_authkey):
                user = self.db.query(User).filter(User.Uid == u_id).one()
                user.Ubirthday = birthday
                self.db.commit()
                self.retjson['contents'] = '修改生日成功'
                self.retjson['code'] = '10521'
            else:
                self.retjson['contents'] = '用户授权码不正确'
                self.retjson['code'] = '10514'

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

