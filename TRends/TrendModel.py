# -*- coding: utf-8 -*-
'''
@author:杨兴才
@模块功能：请求动态
'''
from sqlalchemy import desc
from Database.tables import Trend, TrendImage, UserLike
from Database.models import get_db
from FileHandler.AuthkeyHandler import AuthKeyHandler

class TrendModelHandler(object):
    # 用于登录时获取，动态模型
    def get_trendModel(self, uid):
        retdata = []
        trends = get_db().query(Trend).filter(Trend.Tvalid == 1) \
            .order_by(desc(Trend.TsponsT)).limit(10).all()
        timgurl = []
        for trend in trends:
            imgs = get_db().query(TrendImage).filter(TrendImage.TItid == trend.Tid).all()
            for img in imgs:
                timgurl.append(img.TIimgurl)
            self.response_one(uid, trend, timgurl, retdata)
            print timgurl
            timgurl = []
        return retdata

    def response_one(self, u_id, item, url, retdata):
        authkey = AuthKeyHandler()

        l_flag = 0
        try:
            like = get_db().query(UserLike).filter(UserLike.ULlikeid == u_id,
                                                  UserLike.ULlikedid == item.Tsponsorid,
                                                  UserLike.ULvalid == 1).one()
            l_flag = like.ULvalid
        except Exception, e:
            l_flag = 0

        m_trresponse = dict(
            Tid=item.Tid,                                       #动态id
            Tsponsorid=item.Tsponsorid,                         #发布者id
            TsponsT=item.TsponsT.strftime('%Y-%m-%dT%H:%M:%S'), #创建时间
            TcommentN=item.TcommentN,                           #评论数
            TlikeN=item.TlikeN,                                 #点赞数
            Tcontent=item.Tcontent,                             #内容
            Ttitle=item.Ttitle,                                 #标题
            Tsponsorimg=authkey.download_url(item.Tsponsorimg), #用户头像url
            TIimgurl=authkey.download_urls(url),                #动态图片url
            Tualais=item.Tualais,                               #发布者昵称
            Tislike=int(l_flag),                                # 用户是否关注发布者
        )
        retdata.append(m_trresponse)