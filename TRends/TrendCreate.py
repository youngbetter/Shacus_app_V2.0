# -*- coding: utf-8 -*-

'''
@author:杨兴才
@模块功能：创建动态
'''
import time
from sqlalchemy import desc
from BaseHandler import BaseHandler
from Database.tables import Trend, UserImage, User, Image
from Userinfo.Ufuncs import Ufuncs
from FileHandler.ImageHandler import ImageHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
import json

class TrendcreateHandler(BaseHandler):

    retjson = {'code': '400',
               'contents': 'none'}

    #Tsponsorid Tsponsorimg Tcontent Ttitle
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
        if ufunc.judge_user_valid(u_id,u_auth_key):
            #发表动态
            if type == '85001':
                tr_imgs = self.get_argument('imgs')
                try:
                    tr_imgs_json = json.loads(tr_imgs)
                    if tr_imgs_json:
                        retjson_body['auth_key'] = auth_key_handler.generateToken(tr_imgs_json)
                        self.retjson['code'] = '850010'
                        self.retjson['contents'] = retjson_body
                except Exception, e:
                    print "生成凭证失败"
                    self.retjson['code'] = '850012'
                    self.retjson['contents'] = r"生成凭证失败"

            #第二步，存储图片
            elif type == '85002':
                tr_title = self.get_argument('title')
                tr_content = self.get_argument('content')
                tr_imgs = self.get_argument('imgs')
                try:
                    userImg = self.db.query(UserImage).filter(UserImage.UIuid == u_id).all()
                    uheadimg = userImg[0].UIurl
                    print uheadimg
                    user = self.db.query(User).filter(User.Uid == u_id).one()
                    alais = user.Ualais
                    try:
                        new_trend = Trend(
                            Tsponsorid=u_id,
                            Tsponsorimg=uheadimg,
                            Ttitle=tr_title,
                            Tcontent=tr_content,
                            Tualais=alais,
                        )
                        self.db.merge(new_trend)
                        self.db.commit()
                        try:
                            tr_imgs_json = json.loads(tr_imgs)
                            trend = self.db.query(Trend).filter(Trend.Tcontent == tr_content).order_by(desc(Trend.TsponsT)).all()
                            tr_id = trend[0].Tid
                            imghandler.insert_trend_image(tr_imgs_json, tr_id)
                            self.retjson['code'] = '850020'
                            self.retjson['contents'] = r"动态发表成功"
                        except Exception,e:
                            self.retjson['code'] = '850022'
                            self.retjson['contents'] = r"动态图片插入失败"
                    except Exception,e:
                        self.retjson['code'] = '850024'
                        self.retjson['contents'] = r"动态发表失败"
                except Exception,e:
                    print "用户头像图片获取失败"
                    self.retjson['code'] = '850026'
                    self.retjson['contents'] = r"用户头像或昵称获取失败"

            #删除动态
            elif type == '85003':
                tr_id = self.get_argument('tid')
                try:
                    trend = self.db.query(Trend).filter(Trend.Tid == tr_id).one()
                    if trend.Tvalid == True:
                        trend.Tvalid = 0
                        self.db.commit()
                        self.retjson['code'] = '850030'
                        self.retjson['contents'] = r"删除动态成功"
                    else:
                        self.retjson['code'] = '850032'
                        self.retjson['contents'] = r"动态已经删除过，请勿重复删除"
                except Exception,e:
                    self.retjson['code'] = '850034'
                    self.retjson['contents'] = r"此动态不存在"
        else:
            self.retjson['code'] = '850000'
            self.retjson['contents'] = '用户验证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))