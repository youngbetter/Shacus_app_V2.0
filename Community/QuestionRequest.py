# -*- coding: utf-8 -*-
'''
@author:杨兴才
@模块功能：请求社区问题
'''
import json
from sqlalchemy import desc, and_
from ConstVal.const import Const
from BaseHandler import BaseHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import CommuQuestion, CommuQuesImg, CQCollect, CQcomment, Favorite


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
                        self.response_one(u_id, question, cqimgurl, retdata)
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
                        self.response_one(u_id, question, cqimgurl, retdata)
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
                        self.response_one(u_id, question, cqimgurl, retdata)
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
                        .filter(and_(CQCollect.CQColluid == u_id, CQCollect.CQCollvalid == 1, CQCollect.CQCollid < last_collid))\
                        .order_by(desc(CQCollect.CQCollT)).limit(10).all()
                    cqimgurl = []
                    for coll in colls:
                        question = self.db.query(CommuQuestion) \
                            .filter(and_(CommuQuestion.CQuesid == coll.CQCollquesid, CommuQuestion.CQvalid == 1)).one()
                        imgs = self.db.query(CommuQuesImg).filter(CommuQuesImg.CQquesid == question.CQuesid).all()
                        for img in imgs:
                            cqimgurl.append(img.CQimurl)
                        self.response_one(u_id, question, cqimgurl, retdata)
                        cqimgurl = []
                    self.retjson['code'] = '850570'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.retjson['code'] = '850572'
                    self.retjson['contents'] = '收藏问题加载失败'

            #请求问题模型
            elif type == '85059':
                cq_id = self.get_argument('cqid')
                data = {'Question':'None',
                        'Comments':'None'
                }
                authkey = AuthKeyHandler()
                try:
                    question = self.db.query(CommuQuestion).filter(CommuQuestion.CQuesid == cq_id).one()
                    imgs = self.db.query(CommuQuesImg).filter(CommuQuesImg.CQquesid == question.CQuesid).all()
                    cqimgurl = []
                    for img in imgs:
                        cqimgurl.append(img.CQimurl)
                    self.response_one(u_id, question, cqimgurl, retdata)
                    data['Question'] = retdata
                    try:
                        comments = self.db.query(CQcomment) \
                            .filter(and_(CQcomment.CQcmtquesid == cq_id, CQcomment.CQcmtvalid == 1)) \
                            .order_by(desc(CQcomment.CQcmtT)).limit(10).all()
                        if comments:
                            print "in comment"
                            cmts = []
                            for comment in comments:
                                valid = 1
                                if comment.CQcmtvalid == False:
                                   valid = 0
                                cmt = dict(
                                    CQcmtid=comment.CQcmtid,            #评论id
                                    CQcmtquesid=comment.CQcmtquesid,    #评论对应id
                                    CQcmtcontent=comment.CQcmtcontent,  #评论内容
                                    CQcmtT=comment.CQcmtT.strftime('%Y-%m-%dT%H:%M:%S'),                #评论时间
                                    CQcmtvalid=valid,                                                   #评论是否有效
                                    CQcmtuid=comment.CQcmtuid,
                                    CQcmtuimurl=authkey.download_url(comment.CQcmtuimurl),              #用户头像url
                                    CQcmtualais=comment.CQcmtualais,                                    #用户昵称
                                )
                                cmts.append(cmt)
                            data['Comments'] = cmts
                            self.retjson['code'] = '850590'
                            self.retjson['contents'] = data
                        else:
                            print "毫无评论"
                            self.retjson['code'] = '850596'
                            self.retjson['contents'] = data
                    except Exception,e:
                        self.retjson['code'] = '850592'
                        self.retjson['contents'] = data
                except Exception,e:
                    self.retjson['code'] = '850594'
                    self.retjson['contents'] = r"问题查找失败"
        else:
            self.retjson['code'] = '850500'
            self.retjson['contents'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

    def response_one(self, u_id, item, url, retdata):
        authkey = AuthKeyHandler()
        flag = 0
        f_flag = 0
        try:
            isCollect = self.db.query(CQCollect)\
                .filter(and_(CQCollect.CQColluid == item.CQuid,
                             CQCollect.CQCollquesid == item.CQuesid,)).one()
            flag = isCollect.CQCollvalid
            isFavorite = self.db.query(Favorite)\
                .filter(and_(Favorite.Ftypeid == item.CQuesid,
                             Favorite.Ftype == Const.FAVORITE_TYPE_QUESTION,
                             Favorite.Fuid == u_id)).one()
            f_flag = isFavorite.Fvalid

            if f_flag == True:
                f_flag = 1
            else:
                f_flag = 0

            if flag == True:
                flag = 1
            else:
                flag = 0
        except Exception,e:
            print e
            print "没有收藏点赞记录"
        m_cqresponse = dict(
            CQuesid=item.CQuesid,                               #问题id
            CQuid=item.CQuid,                                   #用户id
            CQtime=item.CQtime.strftime('%Y-%m-%dT%H:%M:%S'),   #问题创建时间
            CQcommentN=item.CQcommentN,                         #问题评论数
            CQlikedN=item.CQlikedN,                             #问题点赞数
            CQcontent=item.CQcontent,                           #问题内容
            CQtitle=item.CQtitle,                               #问题标题
            CQuimurl=authkey.download_url(item.CQuimurl),       #用户头像url
            CQuname=item.CQualais,                              #用户昵称
            CQimgurl=authkey.download_urls(url),                #问题图片urls
            CQuiscollect=int(flag),                                  #用户是否收藏此问题
            CQuisfavorite=int(f_flag),                               #用户是否点赞此问题
        )
        retdata.append(m_cqresponse)
