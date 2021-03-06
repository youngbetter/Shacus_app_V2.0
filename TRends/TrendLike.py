# -*- coding: utf-8 -*-

'''
@author:杨兴才
@模块功能：动态点赞
'''
import json
from sqlalchemy import and_
from BaseHandler import BaseHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import Trend, Favorite
from ConstVal.const import Const

class TrendlikeHandler(BaseHandler):
    retjson = {'code': '200',
               'contents': 'none'}
    def post(self):

        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        t_id = self.get_argument('tid')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功
            #点赞
            if type == '85031':
                try:
                    favorite = self.db.query(Favorite).\
                        filter(and_(Favorite.Ftype == Const.FAVORITE_TYPE_TREND,
                                    Favorite.Ftypeid == t_id)).one()
                    if favorite.Fvalid == 0:
                        try:
                            favorite.Fvalid = 1
                            trend = self.db.query(Trend).filter(Trend.Tid == t_id).one()
                            trend.TlikeN += 1
                            self.db.commit()
                        except Exception,e:
                            self.retjson['code'] = '850316'
                            self.retjson['contents'] = '点赞数据插入失败'
                    else:
                        self.retjson['code'] = '850314'
                        self.retjson['contents'] = '已经点过赞'
                except Exception,e:
                    try:
                        new_fav = Favorite(
                            Fuid=u_id,
                            Ftype=Const.FAVORITE_TYPE_TREND,
                            Ftypeid=t_id
                        )
                        trend = self.db.query(Trend).filter(Trend.Tid == t_id).one()
                        trend.TlikeN += 1
                        self.db.merge(new_fav)
                        self.db.commit()
                        self.retjson['code'] = '850310'
                        self.retjson['contents'] = '点赞成功'
                    except Exception,e:
                        self.retjson['code'] = '850312'
                        self.retjson['contents']= '点赞新增失败'
            #取消点赞
            elif type == '85033':
                try:
                    favorite = self.db.query(Favorite). \
                        filter(and_(Favorite.Ftype == Const.FAVORITE_TYPE_TREND,
                                    Favorite.Ftypeid == t_id)).one()
                    if favorite.Fvalid == 1:
                        try:
                            favorite.Fvalid = 0
                            trend = self.db.query(Trend).filter(Trend.Tid == t_id).one()
                            trend.TlikeN -= 1
                            self.db.commit()
                            self.retjson['code'] = '850336'
                            self.retjson['contents'] = '取消点赞成功'
                        except Exception, e:
                            self.retjson['code'] = '850332'
                            self.retjson['contents'] = '取消点赞失败'
                    else:
                        self.retjson['code'] = '850334'
                        self.retjson['contents'] = '已经取消过点赞'
                except Exception, e:
                    self.retjson['code'] = '850330'
                    self.retjson['contents'] = '没有点赞过'
        else:
            self.retjson['code'] = '850300'
            self.retjson['contents'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))