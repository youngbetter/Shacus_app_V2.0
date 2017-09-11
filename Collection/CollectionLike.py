# -*- coding: utf-8 -*-

'''
@author:杨兴才
@模块功能：作品集点赞
'''
import json
from sqlalchemy import and_
from BaseHandler import BaseHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import UserCollection, Favorite
from ConstVal.const import Const

class CollLikeHandler(BaseHandler):
    retjson = {'code': '200',
               'contents': 'none'}
    def post(self):

        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        coll_id = self.get_argument('collid')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功
            #点赞作品集
            if type == '85091':
                try:
                    favorite = self.db.query(Favorite).\
                        filter(and_(Favorite.Ftype == Const.FAVORITE_TYPE_COLLECT,
                                    Favorite.Ftypeid == coll_id)).one()
                    if favorite.Fvalid == 0:
                        try:
                            favorite.Fvalid = 1
                            coll = self.db.query(UserCollection).filter(UserCollection.UCid == coll_id).one()
                            coll.UClikeN += 1
                            self.db.commit()
                        except Exception,e:
                            self.retjson['code'] = '850916'
                            self.retjson['contents'] = '点赞数据插入失败'
                    else:
                        self.retjson['code'] = '850914'
                        self.retjson['contents'] = '已经点过赞'
                except Exception,e:
                    try:
                        new_fav = Favorite(
                            Fuid=u_id,
                            Ftype=Const.FAVORITE_TYPE_COLLECT,
                            Ftypeid=coll_id
                        )
                        coll = self.db.query(UserCollection).filter(UserCollection.UCid == coll_id).one()
                        coll.UClikeN += 1
                        self.db.merge(new_fav)
                        self.db.commit()
                        self.retjson['code'] = '850910'
                        self.retjson['contents'] = '点赞成功'
                    except Exception,e:
                        self.retjson['code'] = '850912'
                        self.retjson['contents'] = '点赞新增失败'
            #取消点赞
            elif type == '85093':
                try:
                    favorite = self.db.query(Favorite). \
                        filter(and_(Favorite.Ftype == Const.FAVORITE_TYPE_COLLECT,
                                    Favorite.Ftypeid == coll_id)).one()
                    if favorite.Fvalid == 1:
                        try:
                            favorite.Fvalid = 0
                            coll = self.db.query(UserCollection).filter(UserCollection.UCid == coll_id).one()
                            coll.UClikeN -= 1
                            self.db.commit()
                            self.retjson['code'] = '850930'
                            self.retjson['contents'] = '取消点赞成功'
                        except Exception, e:
                            self.retjson['code'] = '850932'
                            self.retjson['contents'] = '取消点赞失败'
                    else:
                        self.retjson['code'] = '850934'
                        self.retjson['contents'] = '已经取消过点赞'
                except Exception, e:
                    self.retjson['code'] = '850936'
                    self.retjson['contents'] = '没有点赞过'
        else:
            self.retjson['code'] = '850900'
            self.retjson['contents'] = '用户验证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))