# coding=utf-8
"""
 @author: ye,young
 2017.9.11
 @模块功能：创建问题
"""
# -*- coding: utf-8 -*-
import time
from sqlalchemy import desc,and_
from BaseHandler import BaseHandler
from Database.tables import UserImage, User, Image, UserCollection, UserCollectionimg
from Userinfo.Ufuncs import Ufuncs
from FileHandler.ImageHandler import ImageHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
import json

class CollcreateHandler(BaseHandler):

    retjson = {'code': '400',
               'contents': 'none'}
    def post(self):
        u_id = self.get_argument('uid')
        u_auth_key = self.get_argument('authkey')
        type = self.get_argument('type')

        #返回客户端上传图片的凭证
        auth_key_handler = AuthKeyHandler()
        retjson_body = {}
        #将图片插入数据库的工具
        imghandler = ImageHandler()
        #用户鉴权
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):
            #创建作品集
            if type == '85081':
                coll_imgs = self.get_argument('imgs')
                try:
                    # query.one()/all()
                    userImg = self.db.query(UserImage).filter(UserImage.UIuid == u_id).one()
                    uheadimg = userImg.UIurl
                    user = self.db.query(User).filter(User.Uid == u_id).one()
                    alais = user.Ualais
                    try:
                        new_coll = UserCollection(
                            UCuid=u_id,
                            UCuimurl=uheadimg,
                            UCualais=alais,
                        )
                        self.db.merge(new_coll)
                        #存储图片
                        try:
                            self.db.commit()
                            tr_imgs_json = json.loads(coll_imgs)
                            if tr_imgs_json:
                                print "uid:"+u_id
                                coll = self.db.query(UserCollection).filter(UserCollection.UCuid == u_id).all()
                                imghandler.insert_collect_image(tr_imgs_json, coll[-1].UCid)
                                self.retjson['code'] = '850810'
                                retjson_body['auth_key'] = auth_key_handler.generateToken(tr_imgs_json)
                                self.retjson['contents'] = retjson_body
                        except Exception, e:
                            print "作品集图片插入失败"
                            self.retjson['code'] = '850812'
                            self.retjson['contents'] = '作品集图片插入失败'
                    except Exception,e:
                        print "作品集发表失败"
                        self.retjson['code'] = '850814'
                        self.retjson['contents'] = '作品集发表失败'
                except Exception,e:
                    print "用户头像图片获取失败"
                    self.retjson['code'] = '850816'
                    self.retjson['contents'] = '用户头像图片获取失败'

            # 删除作品集
            elif type == '85083':
                coll_id = self.get_argument('collid')
                try:
                    coll = self.db.query(UserCollection).filter(UserCollection.UCid == coll_id).one()
                    if coll.UCvalid == True:
                        coll.UCvalid = 0
                        self.db.commit()
                        self.retjson['code'] = '850830'
                        self.retjson['contents'] = r"删除作品集成功"
                    else:
                        self.retjson['code'] = '850832'
                        self.retjson['contents'] = r"作品集已经删除过，请勿重复删除"
                except Exception, e:
                    self.retjson['code'] = '850834'
                    self.retjson['contents'] = r"此作品不存在"

            elif type == '85085':
                pass
        else:
            self.retjson['code'] = '850800'
            self.retjson['contents'] = '用户验证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))