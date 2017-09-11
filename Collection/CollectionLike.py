# coding=utf-8
# 用户作品集模型
import json
import threading
from BaseHandler import BaseHandler
from Userinfo.Ufuncs import Ufuncs
from Database.models import get_db
from Database.tables import User, UserHomepageimg, UserCollection, UClike, UCcomment
from FileHandler.Upload import AuthKeyHandler
from Userinfo.UserImgHandler import UserImgHandler


class CollectionLikeHandler(BaseHandler):
    retjson = {'code': '', 'contents': ""}

    def post(self):
        type = self.get_argument('type', default='unsolved')
        u_id = self.get_argument('uid', default='null')
        u_auth_key = self.get_argument('authkey', default='null')
        uc_id = self.get_argument('ucid')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 认证成功

            # 作品集点赞/取消赞

            try:

                User_Collection = self.db.query(UserCollection).filter(UserCollection.UCid == uc_id).one()
                print User_Collection.UClikeNum

                try:
                    once_liked = self.db.query(UClike).filter(UClike.UClikeUserid == u_id,
                                                              UClike.UClikeid == uc_id).one()
                    print once_liked.UClikeUserid
                    if once_liked:  # 找到了对应的作品集
                        if once_liked.UCLvalid == 1:
                            if type == '80010':  # 对作品集进行点赞
                                self.retjson['code'] = '800100'
                                self.retjson['contents'] = r'已点过赞'
                            elif type == '80011':  # 取消赞
                                once_liked.UCLvalid = 0
                                User_Collection.UClikeNum -= 1
                                self.db.commit()
                                self.retjson['code'] = '800110'
                                self.retjson['contents'] = r'取消赞成功'

                        else:  # 点过赞但是取消了once_liked.UCLvalid == 0
                            if type == '80010':
                                once_liked.UCLvalid = 1
                                User_Collection.UClikeNum += 1
                                self.db.commit()
                                self.retjson['code'] = '800101'
                                self.retjson['contents'] = '点赞成功'
                            elif type == '80011':
                                self.retjson['code'] = '800111'
                                self.retjson['contents'] = r'用户已取消赞！'
                # 没有找到类似点赞记录
                except Exception, e:
                    print 'new like for a collection'
                    if type == '80011':
                        self.retjson['code'] = '800112'
                        self.retjson['contents'] = r'用户未赞过此约拍！'
                    elif type == '80010':
                        new_UClike = UClike(
                            UClikeid=uc_id,
                            UCLvalid=1,
                            UClikeUserid=u_id,
                        )
                        try:
                            User_Collection.UClikeNum += 1
                            self.db.merge(new_UClike)
                            self.db.commit()
                            self.retjson['code'] = '800101'
                            self.retjson['contents'] = '点赞成功'
                        except Exception, e:
                            self.retjson['code'] = '800102'
                            self.retjson['contents'] = '数据库修改失败'
            except Exception, e:
                print e
                self.retjson['code'] = '800103'
                self.retjson['contents'] = '未找到此作品集'
        else:
            print'认证错误'
            self.retjson['code'] = '800104'
            self.retjson['contents'] = '用户认证错误'


        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
