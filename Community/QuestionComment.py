# -*- coding: utf-8 -*-

'''
@author:杨兴才
@模块功能：创建问题评论
'''
import json
import time
from sqlalchemy import and_
from BaseHandler import BaseHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import CQcomment, CommuQuestion

class CQCmtHandler(BaseHandler):
    retjson = {'code': '200',
               'contents': 'null'}
    def post(self):
        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        cq_id = self.get_argument('cqid')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功
            #发布问题评论
            if type == '85061':
                cq_content = self.get_argument('content')
                try:
                    print "1"
                    question = self.db.query(CommuQuestion).filter(CommuQuestion.CQuesid == cq_id).one()
                    print question.CQuesid
                    #相应动态存在并且有效
                    if question.CQvalid == True:
                        try:
                            new_CQcmt = CQcomment(
                                CQcmtquesid=cq_id,
                                CQcmtcontent=cq_content,
                            )
                            print new_CQcmt
                            question.CQcommentN += 1
                            self.db.merge(new_CQcmt)
                            self.db.commit()
                            self.retjson['code'] = '850610'
                            self.retjson['contents'] = '评论发表成功'
                        except Exception,e:
                            print e
                            self.retjson['code'] = '850612'
                            self.retjson['contents'] = '评论发表失败'
                    else:
                        self.retjson['code'] = '850614'
                        self.retjson['contents'] = '要评论的动态不存在或已删除'
                except Exception,e:
                    self.retjson['code'] = '850616'
                    self.retjson['contents'] = '要评论的动态不存在或已删除'
            #删除动态评论
            elif type == '85063':
                cqcmt_id = self.get_argument('cmtid')
                try:
                    cmt = self.db.query(CQcomment).filter(CQcomment.CQcmtid == cqcmt_id).one()
                    if cmt.CQcmtvalid == 0:
                        self.retjson['code'] = '850630'
                        self.retjson['contents'] = '评论已删除过'
                    else:
                        question = self.db.query(CommuQuestion).filter(CommuQuestion.CQuesid == cq_id).one()
                        cmt.CQcmtvalid = 0
                        question.CQcommentN -= 1
                        self.db.commit()
                        self.retjson['code'] = '850632'
                        self.retjson['contents'] = '评论删除成功'
                except Exception, e:
                    self.retjson['code'] = '850634'
                    self.retjson['contents'] = '评论删除失败'
        else:
            self.retjson['code'] = '850600'
            self.retjson['contents'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
