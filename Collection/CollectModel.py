# -*- coding: utf-8 -*-
'''
@author:杨兴才
@模块功能：请求作品集
'''
from sqlalchemy import desc, and_
from Database.tables import UserCollection, UserCollectionimg
from Database.models import get_db
from FileHandler.AuthkeyHandler import AuthKeyHandler

class CollModelHandler(object):
    # 用于登录时获取，作品集模型
    def get_collModel(self, uid):
        retdata = []
        colls = get_db().query(UserCollection).filter(and_(UserCollection.UCvalid == 1,
                                                           UserCollection.UCiscollection == 1)) \
            .order_by(desc(UserCollection.UCcreateT)).limit(10).all()
        collimgurl = []
        for coll in colls:
            imgs = get_db().query(UserCollectionimg).filter(UserCollectionimg.UCIuser == coll.UCid).all()
            for img in imgs:
                collimgurl.append(img.UCIurl)
            self.response_one(coll, collimgurl, retdata)
            collimgurl = []
        return retdata

    def response_one(self, item, url, retdata):
        authkey = AuthKeyHandler()
        m_trresponse = dict(
            UCid=item.UCid,                                             #作品集id
            UCuid=item.UCuid,                                           #作品集发布者id
            UCcreateT=item.UCcreateT.strftime('%Y-%m-%dT%H:%M:%S'),     #发布时间
            UCtitle=item.UCtitle,                                       #作品集标题
            UCvalid=item.UCvalid,                                       #作品集是否有效
            UClikeN=item.UClikeN,                                       #作品集获赞数
            UCuimurl=authkey.download_url(item.UCuimurl),               #作品集发布者头像
            UCIurl=authkey.download_urls(url),                          #作品集图片url
            UCualais=item.UCualais,                                     #作品集发布者昵称
        )
        retdata.append(m_trresponse)