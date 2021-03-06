# -*- coding: utf-8 -*-

#!/usr/bin/env python

import tornado.httpserver
import  tornado.ioloop
import  tornado.options
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import define, options

from Activity.ACHandler import ActivityCreate, ActivityRegister
from Activity.ACaskHandler import AskActivity
from Activity.ACentryHandler import AskEntry
#from Appointment.APAskHandler import APaskHandler
#from Appointment.APCreateHandler_new import APcreateHandler
#from Appointment.APRegistHandler import APregistHandler
#from Appointment.APchatCreateHandler import APchatCreateHandler
#from Appointment.APpraseHandler import APprase
#from Appointment.ApCompanionAuthHandler import AcAuthHandler
#from Appointment.ApCompanionHandler import ApCompanionHandler
from Appointment.Ranklist import Ranklist
from Database.models import engine
from ImageCallback import ImageCallback
from Message.Sysmessage import Sysmessage
from Pressuretest import login
from Pressuretest.Simplerequest import Simplerequest
#from RegisterHandler import RegisterHandler
#from Settings import PaswChange
#from TRends.TRendspost import TRendspost
#from TRends.TrendHandler import TrendHandler
#from Userinfo.Userforgotpw import Userforgotpw
from Userinfo.UserCollectionHandler import UserCollectionHandler
from Userinfo.UserFavoriteHandler import UserFavorite
from Userinfo.UserImgHandler import UserImgHandler
from Userinfo.UserIndent import UserIndent
from Userinfo.UserInfo import UserInfo
from Userinfo.UserLike import FindUlike
from Userinfo.UserList import UserList
from Userinfo.Userhomepager import Userhomepager
from Userinfo.Userhpimg import Userhpimg
#from loginHandler import LoginHandler
#added by young
from TRends.TrendCreate import TrendcreateHandler
from TRends.TrendRequest import TrendrequestHandler
from TRends.TrendComment import TrendCmtHandler
from TRends.TrendLike import TrendlikeHandler
from Community.QuestionCreate import QuestioncreateHandler
from Community.QuestionRequest import CQrequestHandler
from Community.QuestionComment import CQCmtHandler
from Community.QuestionLike import CQlikeHandler
from Community.QuestionCollect import CQCollectHandler

from Collection.CollectionLike import CollLikeHandler
from Collection.CollectionCreate import CollcreateHandler
from Collection.CollectionRequest import CollrequestHandler
# added by ye
from Login.login import LoginHandler
from register import RegisterHandler
from Login.UserForgotPassword import ForgotPasswordHandler
from Settings import PswChange
from Appointment.GetList import GetListHandler
from Appointment.APCreate import APCreateHandler
from Appointment.APRegist import APRegistHandler
from Appointment.APCompanion import ApCompanionHandler
from Appointment.APCompanionAuth import AcAuthHandler
from Appointment.ChooseOne import ChooseOneHandler
#from Collection.CollectionLike import CollectionLikeHandler


define("port", default=800, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
             (r"/pressuretest",Simplerequest),
             (r"/pressuretest2", login.login),
             (r"/user/homepager",Userhomepager),
             (r"/user/mylike", FindUlike),  # updated by ye
             (r"/user/favorite", UserFavorite),
             (r"/user/info",UserInfo),
             (r"/user/indent",UserIndent),
             (r"/Activity/ask", AskActivity),
             (r"/Activity/entry", AskEntry),
             (r"/activity/create", ActivityCreate),
             (r"/activity/register",ActivityRegister),
             (r"/ImageCallback",ImageCallback),
             (r"/ranklist", Ranklist),
             (r"/Userinfo/imghandler",Userhpimg),
             (r"/Userinfo/CollectionHandler",UserCollectionHandler),
             (r"/sysmessage",Sysmessage),
             (r"/recommend/reclist",UserList),
             #added by young
             (r"/trend/creatTrend", TrendcreateHandler),            #创建动态
             (r"/trend/requestTrend", TrendrequestHandler),         #请求动态
             (r"/trend/commentTrend", TrendCmtHandler),             #评论动态
             (r"/trend/likeTrend", TrendlikeHandler),               #动态点赞
             (r"/community/createQuestion", QuestioncreateHandler), #创建问题
             (r"/community/requestQuestion", CQrequestHandler),     #获取问题
             (r"/community/commentQuestion", CQCmtHandler),         #评论问题
             (r"/community/likeQuestion", CQlikeHandler),           #给问题点赞
             (r"/community/collectQuestion", CQCollectHandler),     #收藏问题
             (r"/collection/likeCollection", CollLikeHandler),
             (r"/collection/createCollect", CollcreateHandler),
             (r"/collection/requestCollect", CollrequestHandler),
             # added by ye
             (r"/regist", RegisterHandler),
             (r"/login", LoginHandler),
             (r"/login/forgotpw", ForgotPasswordHandler),
             (r"/PswChange", PswChange),
             (r"/appointment/create", APCreateHandler),
             (r"/appointment/list", GetListHandler),
             (r"/appointment/regist", APRegistHandler),
             (r"/appointment/companion", ApCompanionHandler),
             (r"/companion/getauth", AcAuthHandler),
             (r"/appointment/choose", ChooseOneHandler),

        ]
        tornado.web.Application.__init__(self, handlers)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))

# session负责执行内存中的对象和数据库表之间的同步工作 Session类有很多参数,使用sessionmaker是为了简化这个过程
if __name__ == "__main__":
    print "HI,I am in main "
    tornado.options.parse_command_line()
    Application().listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()

