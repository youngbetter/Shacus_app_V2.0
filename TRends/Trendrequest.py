# -*- coding: utf-8 -*-
'''
@author:杨兴才
@模块功能：请求动态
'''
import json
import TRfunction
from sqlalchemy import desc
from BaseHandlerh import BaseHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import Trend, TrendImage, Image, Favorite


class Trendrequest(BaseHandler):
    retjson = {'code': '200',
               'contents': 'null'}

    def post(self):
        retdata = []
        # 记录上次请求的最后一条动态id
        last_tid = 0
        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')

        # 请求刷新所有动态，下拉
        if type == '12001':
            ufuncs = Ufuncs()  # 判断用户权限
            if ufuncs.judge_user_valid(u_id, u_auth_key):  # 认证成功
                try:
                    trends = self.db.query(Trend).limit(10).order_by(desc(Trend.TsponsT)).all()
                    for trend in trends:
                        img_urls = self.db.query(TrendImage).filter(Trend.Tid == trend.Tid).all()
                        for url in img_urls:
                            self.response_one(trend, url, retdata)
                    last_tid = trend.Tid
                    print last_tid
                except Exception, e:
                    self.retjson['code'] = '12012'
                    self.retjson['contents'] = '用户认证失败'
            else:
                self.retjson['code'] = '12012'
                self.retjson['contents'] = '用户认证失败'
        # 请求刷新所有动态，上拉
        elif type == '500201':
            ufuncs = Ufuncs()  # 判断用户权限
            if ufuncs.judge_user_valid(u_id, u_auth_key):  # 认证成功
                try:
                    trends = self.db.query(Trend).limit(10).filter(Trend.Tid < last_tid).order_by(
                        desc(Trend.TsponsT)).all()
                    for trend in trends:
                        img_urls = self.db.query(TrendImage).filter(Trend.Tid == trend.Tid).all()
                        for url in img_urls:
                            self.response_one(trend, url, retdata)
                except Exception, e:
                    self.retjson['code'] = '12012'
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
