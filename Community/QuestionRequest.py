# -*- coding: utf-8 -*-
'''
@author:杨兴才
@模块功能：请求社区问题
'''
import json
from sqlalchemy import desc

from BaseHandler import BaseHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import CommuQuestion, CommuQuesImg


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
                    questions = self.db.query(CommuQuestion).order_by(desc(CommuQuestion.CQtime)).limit(10).all()
                    print questions[0].CQuesid
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
                    questions = self.db.query(CommuQuestion).filter(CommuQuestion.CQuesid < last_cqid).order_by(desc(CommuQuestion.CQtime)).limit(10).all()
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
