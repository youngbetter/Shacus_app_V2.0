# -*- coding: utf-8 -*-

'''
@author:杨兴才
@模块功能：问题点赞
'''
import json
from sqlalchemy import and_
from BaseHandler import BaseHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import CommuQuestion, Favorite
from ConstVal.const import Const

class CQlikeHandler(BaseHandler):
    retjson = {'code': '200',
               'contents': 'none'}
    def post(self):

        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        cq_id = self.get_argument('cqid')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功
            #点赞
            if type == '85071':
                try:
                    favorite = self.db.query(Favorite).\
                        filter(and_(Favorite.Ftype == Const.FAVORITE_TYPE_QUESTION,
                                    Favorite.Ftypeid == cq_id)).one()
                    if favorite.Fvalid == 0:
                        try:
                            favorite.Fvalid = 1
                            question = self.db.query(CommuQuestion).filter(CommuQuestion.CQuesid == cq_id).one()
                            question.CQlikedN += 1
                            self.db.commit()
                        except Exception,e:
                            self.retjson['code'] = '850716'
                            self.retjson['contents'] = '点赞数据插入失败'
                    else:
                        self.retjson['code'] = '850714'
                        self.retjson['contents'] = '已经点过赞'
                except Exception,e:
                    try:
                        new_fav = Favorite(
                            Fuid=u_id,
                            Ftype=Const.FAVORITE_TYPE_QUESTION,
                            Ftypeid=cq_id
                        )
                        question = self.db.query(CommuQuestion).filter(CommuQuestion.CQuesid == cq_id).one()
                        question.CQlikedN += 1
                        self.db.merge(new_fav)
                        self.db.commit()
                        self.retjson['code'] = '850710'
                        self.retjson['contents'] = '点赞成功'
                    except Exception,e:
                        self.retjson['code'] = '850712'
                        self.retjson['contents']= '点赞新增失败'
            #取消点赞
            elif type == '85073':
                try:
                    favorite = self.db.query(Favorite). \
                        filter(and_(Favorite.Ftype == Const.FAVORITE_TYPE_QUESTION,
                                    Favorite.Ftypeid == cq_id)).one()
                    if favorite.Fvalid == 1:
                        try:
                            favorite.Fvalid = 0
                            question = self.db.query(CommuQuestion).filter(CommuQuestion.CQuesid == cq_id).one()
                            question.CQlikedN -= 1
                            self.db.commit()
                            self.retjson['code'] = '850736'
                            self.retjson['contents'] = '取消点赞成功'
                        except Exception, e:
                            self.retjson['code'] = '850732'
                            self.retjson['contents'] = '取消点赞失败'
                    else:
                        self.retjson['code'] = '850734'
                        self.retjson['contents'] = '已经取消过点赞'
                except Exception, e:
                    self.retjson['code'] = '850700'
                    self.retjson['contents'] = '没有点赞过'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))