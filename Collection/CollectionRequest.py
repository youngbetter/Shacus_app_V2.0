# -*- coding: utf-8 -*-
'''
@author:杨兴才
@模块功能：请求作品集
'''
import json
from sqlalchemy import desc, and_

from BaseHandler import BaseHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import UserCollection, UserCollectionimg


class CollrequestHandler(BaseHandler):
    retjson = {'code': '200',
               'contents': 'null'}

    def post(self):
        retdata = []
        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功
            # 请求刷新所有作品，下拉
            if type == '85101':
                try:
                    colls = self.db.query(UserCollection)\
                        .filter(and_(UserCollection.UCvalid == 1, UserCollection.UCiscollection == 1))\
                        .order_by(desc(UserCollection.UCcreateT)).limit(10).all()
                    ucimgurl = []
                    for coll in colls:
                        imgs = self.db.query(UserCollectionimg).filter(UserCollectionimg.UCIuser == coll.UCid).all()
                        for img in imgs:
                            ucimgurl.append(img.UCIurl)
                        self.response_one(coll, ucimgurl, retdata)
                        print ucimgurl
                        ucimgurl = []
                    self.retjson['code'] = '851010'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.retjson['code'] = '851012'
                    self.retjson['contents'] = '作品集刷新失败'

            # 请求刷新所有作品集，上拉
            elif type == '85103':
                try:
                    last_ucid = self.get_argument('lastid')
                    print last_ucid
                    colls = self.db.query(UserCollection)\
                        .filter(and_(UserCollection.UCid < last_ucid, UserCollection.UCvalid == 1, UserCollection.UCiscollection == 1))\
                        .order_by(desc(UserCollection.UCcreateT)).limit(10).all()
                    ucimgurl = []
                    for coll in colls:
                        imgs = self.db.query(UserCollectionimg).filter(UserCollectionimg.UCIuser == coll.UCid).all()
                        for img in imgs:
                            ucimgurl.append(img.UCIurl)
                        self.response_one(coll, ucimgurl, retdata)
                        print ucimgurl
                        ucimgurl = []
                    self.retjson['code'] = '851030'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.retjson['code'] = '851032'
                    self.retjson['contents'] = '作品集加载失败'

            #请求个人照片
            elif type == '85105':
                try:
                    privites = self.db.query(UserCollection)\
                        .filter(and_(UserCollection.UCuid == u_id, UserCollection.UCiscollection == 0, UserCollection.UCvalid == 1))\
                        .order_by(desc(UserCollection.UCcreateT)).limit(10).all()
                    priimgs = []
                    for privite in privites:
                        imgs = self.db.query(UserCollectionimg).filter(UserCollectionimg.UCIuser == privite.UCid).all()
                        for img in imgs:
                            priimgs.append(img.UCIurl)
                        self.response_one(privite, priimgs, retdata)
                        priimgs = []
                        self.retjson['code'] = '851050'
                        self.retjson['contents'] = retdata
                except Exception,e:
                    self.retjson['code'] = '851052'
                    self.retjson['contents'] = '个人照片加载失败'
        else:
            self.retjson['code'] = '851000'
            self.retjson['contents'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

    def response_one(self, item, url, retdata):
        authkey = AuthKeyHandler()
        m_collresponse = dict(
            UCid=item.UCid,
            UCuid=item.UCuid,
            UCcreateT=item.UCcreateT.strftime('%Y-%m-%dT%H:%M:%S'),
            UCiscollection=item.UCiscollection,
            UClikeN=item.UClikeN,
            UCuimurl=authkey.download_url(item.UCuimurl),
            UCIurl=authkey.download_urls(url),
            UCualais=item.UCualais,
        )
        retdata.append(m_collresponse)
