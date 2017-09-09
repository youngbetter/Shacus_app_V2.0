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

class TrendLikeHandler(BaseHandler):
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
            if type == '82031':
                try:
                    favorite = self.db.query(Favorite).\
                        filter(and_(Favorite.Ftype == Const.FAVORITE_TYPE_TREND,
                                    Favorite.Ftypeid == t_id)).one()

                except Exception,e:
                    try:
                        new_fav = Favorite(
                            Fuid=u_id,
                            Ftype=Const.FAVORITE_TYPE_TREND,
                            Ftypeid=t_id
                        )
                        self.db.merge(new_fav)
                        self.db.commit()
                    except Exception,e:
                        self.retjson['code'] = '820312'
                        self.retjson['contents']= '点赞新增失败'
                self.retjson['code'] = '820310'
                self.retjson['contents'] = '点赞成功'
        else:
            pass
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))