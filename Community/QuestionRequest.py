# -*- coding: utf-8 -*-
'''
@author:杨兴才
@模块功能：请求社区问题
'''
import json
from sqlalchemy import desc, and_

from BaseHandler import BaseHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import CommuQuestion, CommuQuesImg, CQCollect


class CQrequestHandler(BaseHandler):
    retjson = {'code': '200',
               'contents': 'null'}

    def post(self):
        retdata = []
        # 记录上次请求的最后一条问题id
        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功
            # 请求刷新所有问题，下拉
            if type == '85051':
                try:
                    questions = self.db.query(CommuQuestion).filter(CommuQuestion.CQvalid == 1)\
                        .order_by(desc(CommuQuestion.CQtime)).limit(10).all()
                    cqimgurl = []
                    for question in questions:
                        imgs = self.db.query(CommuQuesImg).filter(CommuQuesImg.CQquesid == question.CQuesid).all()
                        for img in imgs:
                            cqimgurl.append(img.CQimurl)
                        self.response_one(question, cqimgurl, retdata)
                        print cqimgurl
                        cqimgurl = []
                    self.retjson['code'] = '850510'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.retjson['code'] = '850512'
                    self.retjson['contents'] = '问题刷新失败'

            # 请求刷新所有问题，上拉
            elif type == '85053':
                try:
                    last_cqid = self.get_argument('lastid')
                    print last_cqid
                    questions = self.db.query(CommuQuestion)\
                        .filter(and_(CommuQuestion.CQuesid < last_cqid, CommuQuestion.CQvalid == 1))\
                        .order_by(desc(CommuQuestion.CQtime)).limit(10).all()
                    cqimgurl = []
                    for question in questions:
                        imgs = self.db.query(CommuQuesImg).filter(CommuQuesImg.CQquesid == CommuQuestion.CQuesid).all()
                        for img in imgs:
                            cqimgurl.append(img.CQimurl)
                        self.response_one(question, cqimgurl, retdata)
                        print cqimgurl
                        cqimgurl = []
                    self.retjson['code'] = '850530'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.retjson['code'] = '850532'
                    self.retjson['contents'] = '问题加载失败'

            # 请求刷新所收藏问题，下拉
            elif type == '85055':
                try:
                    #筛选
                    #获取每个用户收藏的所有问题
                    colls = self.db.query(CQCollect)\
                        .filter(and_(CQCollect.CQColluid == u_id, CQCollect.CQCollvalid == 1)).order_by(desc(CQCollect.CQCollT)).limit(10).all()
                    cqimgurl = []
                    for coll in colls:
                        question = self.db.query(CommuQuestion)\
                            .filter(and_(CommuQuestion.CQuesid == coll.CQCollquesid, CommuQuestion.CQvalid == 1)).one()
                        imgs = self.db.query(CommuQuesImg).filter(CommuQuesImg.CQquesid == question.CQuesid).all()
                        for img in imgs:
                            cqimgurl.append(img.CQimurl)
                        self.response_one(question, cqimgurl, retdata)
                        cqimgurl = []
                    self.retjson['code'] = '850550'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.retjson['code'] = '850552'
                    self.retjson['contents'] = '收藏问题刷新失败'

            # 请求刷新所收藏问题，上拉
            elif type == '85057':
                try:
                    last_collid = self.get_argument('lastid')
                    # 筛选
                    # 获取每个用户收藏的所有问题
                    colls = self.db.query(CQCollect) \
                        .filter(and_(CQCollect.CQColluid == u_id, CQCollect.CQCollvalid == 1, CQCollect.CQCollid < last_collid)).order_by(
                        desc(CQCollect.CQCollT)).limit(10).all()
                    cqimgurl = []
                    for coll in colls:
                        question = self.db.query(CommuQuestion) \
                            .filter(and_(CommuQuestion.CQuesid == coll.CQCollquesid, CommuQuestion.CQvalid == 1)).one()
                        imgs = self.db.query(CommuQuesImg).filter(CommuQuesImg.CQquesid == question.CQuesid).all()
                        for img in imgs:
                            cqimgurl.append(img.CQimurl)
                        self.response_one(question, cqimgurl, retdata)
                        cqimgurl = []
                    self.retjson['code'] = '850570'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.retjson['code'] = '850572'
                    self.retjson['contents'] = '收藏问题加载失败'
        else:
            self.retjson['code'] = '850500'
            self.retjson['contents'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

    def response_one(self, item, url, retdata):
        authkey = AuthKeyHandler()
        m_cqresponse = dict(
            CQuesid=item.CQuesid,
            CQuid=item.CQuid,
            CQtime=item.CQtime.strftime('%Y-%m-%dT%H:%M:%S'),
            CQcommentN=item.CQcommentN,
            TliCQlikedNkeN=item.CQlikedN,
            CQcontent=item.CQcontent,
            CQtitle=item.CQtitle,
            CQuimurl=authkey.download_url(item.CQuimurl),
            CQimgurl=authkey.download_url(url),
        )
        retdata.append(m_cqresponse)
