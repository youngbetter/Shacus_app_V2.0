# -*- coding: utf-8 -*-
'''
@author:杨兴才
@模块功能：请求动态
'''
import json
from sqlalchemy import desc

from BaseHandler import BaseHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import Trend, TrendImage


class TrendrequestHandler(BaseHandler):
    retjson = {'code': '200',
               'contents': 'null'}

    def post(self):
        retdata = []
        # 记录上次请求的最后一条动态id
        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功
            # 请求刷新所有动态，下拉
            if type == '85013':
                try:
                    trends = self.db.query(Trend).order_by(desc(Trend.TsponsT)).limit(1).all()
                    timgurl = []
                    for trend in trends:
                        imgs = self.db.query(TrendImage).filter(TrendImage.TItid == trend.Tid).all()
                        for img in imgs:
                            timgurl.append(img.TIimgurl)
                        self.response_one(trend, timgurl, retdata)
                        print timgurl
                        timgurl = []
                    self.retjson['code'] = '850130'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.retjson['code'] = '850132'
                    self.retjson['contents'] = '动态刷新失败'

            # 请求刷新所有动态，上拉
            elif type == '85011':
                try:
                    last_tid = self.get_argument('lasttid')
                    print last_tid
                    trends = self.db.query(Trend).filter(Trend.Tid < last_tid).order_by(desc(Trend.TsponsT)).limit(10).all()
                    timgurl = []
                    for trend in trends:
                        imgs = self.db.query(TrendImage).filter(TrendImage.TItid == trend.Tid).all()
                        for img in imgs:
                            timgurl.append(img.TIimgurl)
                        self.response_one(trend, timgurl, retdata)
                        print timgurl
                        timgurl = []
                    self.retjson['code'] = '850110'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.retjson['code'] = '850112'
                    self.retjson['contents'] = '动态加载失败'
        else:
            self.retjson['code'] = '850150'
            self.retjson['contents'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

    def response_one(self, item, url, retdata):
        authkey = AuthKeyHandler()
        m_trresponse = dict(
            Tid=item.Tid,
            Tsponsorid=item.Tsponsorid,
            TsponsT=item.TsponsT.strftime('%Y-%m-%dT%H:%M:%S'),
            TcommentN=item.TcommentN,
            TlikeN=item.TlikeN,
            Tcontent=item.Tcontent,
            Ttitle=item.Ttitle,
            Tsponsorimg=authkey.download_url(item.Tsponsorimg),
            TIimgurl=authkey.download_url(url),
        )
        retdata.append(m_trresponse)
