# -*- coding: utf-8 -*-

'''
@author:杨兴才
@模块功能：创建动态评论
'''
import json
import time
from sqlalchemy import and_
from BaseHandler import BaseHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import TrendComment,Trend

class TrendCmtHandler(BaseHandler):
    retjson = {'code': '200',
               'contents': 'null'}
    def post(self):
        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        t_id = self.get_argument('tid')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功
            #发布动态评论
            if type == '85021':
                tr_content = self.get_argument('content')
                try:
                    trend = self.db.query(Trend).filter(Trend.Tid == t_id).one()
                    #相应动态存在并且有效
                    if trend.Tvalid == True:
                        try:
                            new_trendcmt = TrendComment(
                                TRcmttid=t_id,
                                TRcmtcontent=tr_content,
                            )
                            print new_trendcmt
                            trend.TcommentN += 1
                            self.db.merge(new_trendcmt)
                            self.db.commit()
                            self.retjson['code'] = '850210'
                            self.retjson['contents'] = '评论发表成功'
                        except Exception,e:
                            print e
                            self.retjson['code'] = '850212'
                            self.retjson['contents'] = '评论发表失败'
                    else:
                        self.retjson['code'] = '850216'
                        self.retjson['contents'] = '要评论的动态不存在或已删除'
                except Exception,e:
                    self.retjson['code'] = '850214'
                    self.retjson['contents'] = '要评论的动态不存在或已删除'
            #删除动态评论
            elif type == '85023':
                trcmt_id = self.get_argument('cmtid')
                try:
                    cmt = self.db.query(TrendComment).filter(TrendComment.TRcmtid == trcmt_id).one()
                    if cmt.TRcmtvalid == 0:
                        self.retjson['code'] = '850230'
                        self.retjson['contents'] = '评论已删除过'
                    else:
                        trend = self.db.query(Trend).filter(Trend.Tid == t_id).one()
                        cmt.TRcmtvalid = 0
                        trend.TcommentN -= 1
                        self.db.commit()
                        self.retjson['code'] = '850232'
                        self.retjson['contents'] = '评论删除成功'
                except Exception, e:
                    self.retjson['code'] = '850234'
                    self.retjson['contents'] = '评论删除失败'
        else:
            self.retjson['code'] = '850250'
            self.retjson['contents'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
