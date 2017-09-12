# -*- coding: utf-8 -*-

'''
@author:杨兴才
@模块功能：创建问题
'''
import time
from sqlalchemy import desc,and_
from BaseHandler import BaseHandler
from Database.tables import UserImage, User, Image, CommuQuestion, CommuQuesImg, CQcomment
from Userinfo.Ufuncs import Ufuncs
from FileHandler.ImageHandler import ImageHandler
from FileHandler.AuthkeyHandler import AuthKeyHandler
import json

class QuestioncreateHandler(BaseHandler):

    retjson = {'code': '400',
               'contents': 'none'}
    def post(self):
        u_id = self.get_argument('uid')
        u_auth_key = self.get_argument('authkey')
        type = self.get_argument('type')

        #返回客户端上传图片的凭证
        auth_key_handler = AuthKeyHandler()
        retjson_body = {}
        #将图片插入数据库的工具
        imghandler = ImageHandler()
        #用户鉴权
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):
            if type == '85041':
                cq_imgs = self.get_argument('imgs')
                #生成凭证
                try:
                    tr_imgs_json = json.loads(cq_imgs)
                    if tr_imgs_json:
                        retjson_body['auth_key'] = auth_key_handler.generateToken(tr_imgs_json)
                        self.retjson['code'] = '850410'
                        self.retjson['contents'] = retjson_body
                except Exception, e:
                    print "生成凭证失败"
                    self.retjson['code'] = '850012'
                    self.retjson['contents'] = r"生成凭证失败"

            elif type == '85042':
                cq_title = self.get_argument('title')
                cq_content = self.get_argument('content')
                cq_imgs = self.get_argument('imgs')
                try:
                    # query.one()/all()
                    userImg = self.db.query(UserImage).filter(UserImage.UIuid == u_id).one()
                    uheadimg = userImg.UIurl
                    user = self.db.query(User).filter(User.Uid == u_id).one()
                    alais = user.Ualais
                    print uheadimg
                    try:
                        new_cq = CommuQuestion(
                            CQuid=u_id,
                            CQtitle=cq_title,
                            CQcontent=cq_content,
                            CQuimurl=uheadimg,
                            CQualais=alais,
                        )
                        self.db.merge(new_cq)
                        self.db.commit()
                        try:
                            tr_imgs_json = json.loads(cq_imgs)
                            if tr_imgs_json:
                                question = self.db.query(CommuQuestion). \
                                    filter(and_(CommuQuestion.CQcontent == cq_content, CommuQuestion.CQuid == u_id)) \
                                    .order_by(desc(CommuQuestion.CQtime)).one()
                                cq_id = question.CQuesid
                                imghandler.insert_commuques_image(tr_imgs_json, cq_id)
                                self.retjson['code'] = '850420'
                                retjson_body['auth_key'] = auth_key_handler.generateToken(tr_imgs_json)
                                self.retjson['contents'] = retjson_body
                        except Exception,e:
                            print "社区问题图片插入失败"
                            self.retjson['code'] = '850422'
                            self.retjson['contents'] = '社区问题图片插入失败'
                    except Exception,e:
                        print "社区问题发表失败"
                        self.retjson['code'] = '850424'
                        self.retjson['contents'] = '社区问题发表失败'
                except Exception, e:
                    print "用户头像图片获取失败"
                    self.retjson['code'] = '850426'
                    self.retjson['contents'] = '用户头像图片获取失败'

            # 删除动态
            elif type == '85043':
                cq_id = self.get_argument('cqid')
                try:
                    question = self.db.query(CommuQuestion).filter(CommuQuestion.CQuesid == cq_id).one()
                    if question.CQvalid == True:
                        question.CQvalid = 0
                        self.db.commit()
                        self.retjson['code'] = '850430'
                        self.retjson['contents'] = r"删除问题成功"
                    else:
                        self.retjson['code'] = '850432'
                        self.retjson['contents'] = r"问题已经删除过，请勿重复删除"
                except Exception, e:
                    self.retjson['code'] = '850434'
                    self.retjson['contents'] = r"此问题不存在"
        else:
            self.retjson['code'] = '850400'
            self.retjson['contents'] = '用户验证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))