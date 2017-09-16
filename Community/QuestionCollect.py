# -*- coding: utf-8 -*-

'''
@author:杨兴才
@模块功能：收藏问题
'''
import json
from sqlalchemy import and_
from BaseHandler import BaseHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import CQCollect, CommuQuestion

class CQCollectHandler(BaseHandler):
    retjson = {'code': '200',
               'contents': 'null'}
    def post(self):
        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        cq_id = self.get_argument('cqid')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功
            #收藏问题
            if type == '85111':
                try:
                    question = self.db.query(CommuQuestion).filter(CommuQuestion.CQuesid == cq_id).one()
                    #相应问题存在并且有效
                    if question.CQvalid == True:
                        try:
                            coll = self.db.query(CQCollect).filter(and_(CQCollect.CQColluid == u_id, CQCollect.CQCollquesid == cq_id)).one()
                            if coll.CQCollvalid == 1:
                                self.retjson['code'] = '851118'
                                self.retjson['contents'] = '曾收藏过'
                            else:
                                coll.CQCollvalid = 1
                                self.db.commit()
                                self.retjson['code'] = '851120'
                                self.retjson['contents'] = '重新收藏成功'
                        except Exception, e:
                            try:
                                new_cqcoll = CQCollect(
                                    CQColluid=u_id,
                                    CQCollquesid=cq_id,
                                )
                                print new_cqcoll
                                self.db.merge(new_cqcoll)
                                self.db.commit()
                                self.retjson['code'] = '851110'
                                self.retjson['contents'] = '创建收藏成功'
                            except Exception,e:
                                print e
                                self.retjson['code'] = '851112'
                                self.retjson['contents'] = '收藏失败'
                    else:
                        self.retjson['code'] = '851114'
                        self.retjson['contents'] = '要收藏的问题不存在或已删除'
                except Exception,e:
                    self.retjson['code'] = '851116'
                    self.retjson['contents'] = '要收藏的问题不存在或已删除'
            #取消收藏
            elif type == '85113':
                cqcoll_id = self.get_argument('collid')
                try:
                    coll = self.db.query(CQCollect).filter(CQCollect.CQCollid == cqcoll_id).one()
                    if coll.CQCollvalid == 0:
                        self.retjson['code'] = '851130'
                        self.retjson['contents'] = '曾已取消收藏'
                    else:
                        coll.CQCollvalid = 0
                        self.db.commit()
                        self.retjson['code'] = '851132'
                        self.retjson['contents'] = '取消收藏成功'
                except Exception, e:
                    self.retjson['code'] = '851134'
                    self.retjson['contents'] = '取消收藏失败'
        else:
            self.retjson['code'] = '851100'
            self.retjson['contents'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
