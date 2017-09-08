# -*- coding: utf-8 -*-

'''
@author:杨兴才
@模块功能：创建动态
'''
import time
from sqlalchemy import desc
from BaseHandlerh import BaseHandler
from Database.tables import Trend, UserImage, User, Image
from Userinfo.Ufuncs import Ufuncs
from FileHandler.ImageHandler import ImageHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
import json

class Trendcreat(BaseHandler):

    retjson = {'code': '400',
               'contents': 'none'}

    def insert_failed(self):
        self.retjson['code'] = '500102'
        self.retjson['contents'] = r"数据库插入失败"

    #Tsponsorid Tsponsorimg Tcontent Ttitle
    def post(self):
        u_id = self.get_argument('uid')
        tr_title = self.get_argument('title')
        u_auth_key = self.get_argument('authkey')
        tr_content = self.get_argument('content')
        tr_imgs = self.get_argument('imgs')

        #返回客户端上传图片的凭证
        auth_key_handler = AuthKeyHandler()
        retjson_body = {}
        #将图片插入数据库的工具
        imghandler = ImageHandler()
        #用户鉴权
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id,u_auth_key):
            try:
                # query.one()/all()
                userImg = self.db.query(UserImage).filter(UserImage.UIuid == u_id).all()
                uheadimg = userImg[0].UIurl

                try:
                    new_trend = Trend(
                        Tsponsorid=u_id,
                        Tsponsorimg=uheadimg,
                        Ttitle=tr_title,
                        Tcontent=tr_content
                    )
                    self.db.merge(new_trend)
                    #存储图片
                    try:
                        self.db.commit()
                        tr_imgs_json = json.loads(tr_imgs)
                        if tr_imgs_json:
                            trend = self.db.query(Trend).filter(Trend.Tcontent == tr_content).order_by(desc(Trend.TsponsT)).all()
                            tr_id = trend[0].Tid
                            self.retjson['code'] = '500101'
                            imghandler.insert_trend_image(tr_imgs_json,tr_id)
                            retjson_body['auth_key'] = auth_key_handler.generateToken(tr_imgs_json)
                            self.retjson['contents'] = retjson_body
                    except Exception, e:
                        print "动态图片插入失败"
                        self.insert_failed()
                except Exception,e:
                    print "动态发表失败"
                    self.insert_failed()
            except Exception,e:
                print "用户头像图片获取失败"
                self.insert_failed()
        else:
            self.retjson['code'] = '500104'  # 待定
            self.retjson['contents'] = '用户验证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))