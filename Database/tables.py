# -*- coding: utf-8 -*-


'''
@author: 黄鑫晨 兰威 王佳镭
'''

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData,ForeignKey,DateTime,Boolean
from sqlalchemy.types import CHAR, Integer, VARCHAR,Boolean,Float,Text
from sqlalchemy.sql.functions import func
from models import Base
import sys
reload(sys)

# from models import engine

# 每个类对应一个表
class User(Base):   #用户表   #添加聊天专用chattoken
    __tablename__ = 'User'

    Uid = Column(Integer, nullable=False, primary_key=True) # 主键
    Upassword = Column(VARCHAR(16), nullable=False)
    Utel = Column(CHAR(11),nullable=False,unique=True,)
    Ualais = Column(VARCHAR(24),nullable=False,unique=True) # 昵称
    Uname = Column(VARCHAR(24),nullable=True)               # 真实姓名
    Ulocation = Column(VARCHAR(128))
    Umailbox = Column(VARCHAR(32))                          #unique=True) # unique表示唯一性
    Ubirthday = Column(DateTime)
    Uscore = Column(Integer, default=0)                     #用户评分，用于排名
    UregistT = Column(DateTime(timezone=True), default=func.now())  #注册时间
    Usex = Column(Boolean,nullable=False)
    Usign = Column(VARCHAR(256))                            #用户签名
    Uauthkey = Column(VARCHAR(32))                          #用户授权码，用于七牛云上传下载文件
    Uchattoken = Column(VARCHAR(128), nullable=False)       #融云的chat_token
    Uage = Column(Integer, nullable=False, default=0)
    Ucategory = Column(Integer, nullable=False, default=0)  #用户分类：0-普通用户，1-摄影师，2-模特，3-商家
    UlikedN = Column(Integer, nullable=False, default=0)    #用户总获赞数


class UCinfo(Base):
    __tablename__ = 'UCinfo'

    UCuid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'),nullable=False,primary_key=True)
    UClikeN = Column(Integer, nullable=False, default=0)
    UClikedN = Column(Integer, nullable=False, default=0)
    UCapN = Column(Integer, nullable=False, default=0)
    UCphotoN = Column(Integer, nullable=False, default=0)
    UCcourseN = Column(Integer, nullable=False, default=0)
    UCmomentN = Column(Integer, nullable=False, default=0)

class Verification(Base): # 短信验证码及生成用户auth_key时间
    __tablename__ = 'Verification'
    Vphone = Column(CHAR(11),primary_key=True)
    Vcode = Column(CHAR(6),nullable=False)
    VT = Column(DateTime(timezone=True), default=func.now()) # 待测试：是插入数据的时间还是最后一次更新该表的时间 （测试结果为第一次插入时间）

class CheckIn(Base):    #签到表
    __tablename__ = 'CheckIn'
    # 复合主键
    CIuid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'),primary_key=True)
    CIcheckday = Column(DateTime(timezone=True), default=func.now())
    CIchecked = Column(Boolean, nullable=False, default=0)  #该日是否签到过
    CItotalN = Column(Integer, nullable=False ,default=0)

class UserLike(Base):   #用户关注用户表（粉丝）
    __tablename__ = 'UserLike'

    ULid=Column(Integer,primary_key=True,nullable=False)
    ULlikeid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'),nullable=False)
    ULlikedid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'),nullable=False)
    ULvalid = Column(Boolean, nullable= False, default=1)
    ULlikeT = Column(DateTime(timezone=True), default=func.now())

class Image(Base):  #图片总表
    __tablename__ = 'Image'

    IMid = Column(Integer,primary_key=True,nullable=False)
    IMvalid = Column(Boolean,default=1)
    IMT = Column(DateTime(timezone=True), default=func.now())
    IMname = Column(VARCHAR(128), nullable=False)

class ActivityImage(Base):  #活动图片表
    __tablename__ = "ActivityImage"

    ACIimid = Column(Integer, ForeignKey('Image.IMid', onupdate='CASCADE'), primary_key=True)
    ACIacid = Column(Integer,ForeignKey('Activity.ACid',onupdate='CASCADE'))
    ACIurl = Column(VARCHAR(128))#数据长度

class AppointmentImage(Base):   #约拍图片
    __tablename__ = 'AppointImage'

    APIimid = Column(Integer, ForeignKey("Image.IMid", onupdate="CASCADE"), primary_key=True)
    APIapid = Column(Integer,ForeignKey("Appointment.APid",onupdate="CASCADE"))
    APIurl = Column(VARCHAR(128))

class UserImage(Base):  #用户图片
    __tablename__ = 'UserImage'

    UIimid = Column(Integer, ForeignKey("Image.IMid", onupdate="CASCADE"), primary_key=True)
    UIuid = Column(Integer, ForeignKey("User.Uid", onupdate="CASCADE"))
    UIurl = Column(VARCHAR(128))

class UserHomepageimg(Base):    #用户个人图片展示
    __tablename__ = 'UserHomepageimg'

    UHpageid= Column(Integer, primary_key=True)
    UHuid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))
    UHimgid = Column (Integer, ForeignKey('Image.IMid', onupdate='CASCADE'))
    UHpicurl= Column(VARCHAR(128))
    UHpicvalid = Column(Integer, default=0)
    UHheight = Column(Integer,default=0)
    UHwidth = Column(Integer,default=0)

class TrendImage(Base):
    __tablename__ = 'TrendImage'

    TIid = Column(Integer, primary_key=True)
    TItid = Column (Integer, ForeignKey('Trend.Tid',onupdate='CASCADE'))
    TIimid = Column(Integer, ForeignKey('Image.IMid',onupdate='CASCADE'))
    TIimgurl = Column(VARCHAR(128))

class CommuQuesImg(Base):   #社区问题图片
    __tablename__='CommuQuesImg'

    CQimid = Column(Integer, ForeignKey("Image.IMid", onupdate="CASCADE"), primary_key=True)
    CQquesid = Column(Integer, ForeignKey("CommuQuestion.CQuesid", onupdate="CASCADE"))
    CQimurl = Column(VARCHAR(128))

class CommuQuestion(Base):  #社区问题
    __tablename__="CommuQuestion"

    CQuesid = Column(Integer, primary_key=True , nullable=False)
    CQuid = Column(Integer, ForeignKey("User.Uid", onupdate="CASCADE")) #提出者id
    CQuimurl = Column(VARCHAR(128),nullable=False)
    CQualais = Column(VARCHAR(24), ForeignKey('User.Ualais', onupdate='CASCADE'),nullable=False)    #新增
    CQtitle = Column(VARCHAR(128), nullable=False)
    CQcontent = Column(VARCHAR(128), nullable=False)
    CQtime = Column(DateTime(timezone=True), default=func.now())
    CQvalid = Column(Boolean, nullable=False, default=1)
    CQlikedN = Column(Integer, nullable=False, default=0)               #获赞数
    CQcommentN = Column(Integer, nullable=False, default=0)             #评论数

class CQcomment(Base):  #社区评论
    __tablename__="CQcomment"

    CQcmtid = Column(Integer, primary_key=True , nullable=False)
    CQcmtquesid = Column(Integer, ForeignKey("CommuQuestion.CQuesid", onupdate="CASCADE"))     #社区问题问题id
    CQcmtcontent = Column(VARCHAR(128), nullable=False)
    CQcmtT = Column(DateTime(timezone=True), default=func.now())
    CQcmtvalid = Column(Boolean, nullable=False ,default=1)

class CQLike(Base):
    __tablename__ = 'CQLike'

    CQLid = Column(Integer, primary_key=True)
    CQLquesid = Column(Integer, ForeignKey("CommuQuestion.CQuesid", onupdate="CASCADE"))     #社区问题问题id
    CQLuid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))
    CQLvalid = Column(Boolean, nullable=False, default=1)
    CQLT = Column(DateTime(timezone=True), default=func.now())

class CQCollect(Base):
    __tablename__ = 'CQCollect'

    CQCollid = Column(Integer, primary_key=True)
    CQColluid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))
    CQCollquesid = Column(Integer, ForeignKey("CommuQuestion.CQuesid", onupdate="CASCADE"))  # 社区问题问题id
    CQCollvalid = Column(Boolean, nullable=False, default=1)
    CQCollT = Column(DateTime(timezone=True), default=func.now())

class Appointment(Base):  #摄影师-模特约拍
    __tablename__ = 'Appointment'

    APid = Column(Integer, primary_key=True, nullable=False)
    APsponsorid = Column(Integer, ForeignKey('User.Uid', ondelete='CASCADE'), nullable=False)   #发起者
    # APtitle=Column(VARCHAR(24),nullable=False)
    APlocation = Column(VARCHAR(128), nullable=False,default='南京')
    APtag=Column(VARCHAR(12)) # 约拍标签？确认长度
    # APstartT = Column(DateTime, nullable=False, default='0000-00-00 00:00:00 ')
    # APendT = Column(DateTime, nullable=False, default='0000-00-00 00:00:00 ')
    # APjoinT=Column(DateTime, nullable=False, default='0000-00-00 00:00:00 ')
    APtime = Column(VARCHAR(128), nullable=False, default='')   # 约拍的时间描述
    APcontent=Column(VARCHAR(128), nullable=False, default='')  # 约拍的内容描述
    # APfree = Column(Boolean)
    APpricetag = Column(Integer, nullable=False, default=0)     # 约拍的价格类型 0-免费，1-付费，2-待商议
    APprice = Column(VARCHAR(64))
    APclosed = Column(Boolean,default=0)
    APcreateT = Column(DateTime(timezone=True), default=func.now())
    APtype = Column(Boolean,nullable=False,default=0)           # 约拍类型，0-摄影师约模特,1-模特约摄影师
    APaddallowed = Column(Boolean,default=0)
    # APlikeN = Column(Integer, default=0, nullable=False)
    APvalid = Column(Boolean, default=1, nullable=False)
    APregistN = Column(Integer, nullable=False, default=0)      # 报名人数
    APstatus = Column(Integer, nullable=False, default=0)       # 0-报名中，1-进行中，2-未评价，3-已评价
    APgroup = Column(Integer, nullable=False, default=0)        # 约拍的分类


class AppointmentInfo(Base):
    __tablename__ = "Appointmentinfo"

    AIid = Column(Integer,primary_key=True)
    AImid = Column(Integer,ForeignKey('User.Uid', ondelete='CASCADE'))  #模特id
    AIpid = Column(Integer,ForeignKey('User.Uid', ondelete='CASCADE'))  #摄影师id
    AIappoid = Column(Integer, ForeignKey('Appointment.APid', onupdate='CASCADE'))  # 与AIid相同，是否重复？
    AImscore = Column(Float,default=0)                                  #模特评分
    AIpscore = Column(Float,default=0)                                  #摄影师评分
    AImcomment = Column(VARCHAR(128))                                   #模特评论
    AIpcomment = Column(VARCHAR(128))                                   #摄影师评论

#约拍报名项
class AppointEntry(Base):
    __tablename__ = "AppointEntry"

    AEid = Column(Integer, primary_key=True)
    AEapid = Column(Integer, ForeignKey('Appointment.APid',onupdate='CASCADE'))
    AEregisterID = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))
    AEvalid = Column(Boolean, nullable=False,default=1)
    AEchoosed = Column(Boolean, nullable=False,default=0)
    AEregistT = Column(DateTime(timezone=True), default=func.now())
    AEmessage = Column(VARCHAR(128), nullable=False, default='')

class Favorite(Base):
    __tablename__ = 'Favorite'

    Fid = Column(Integer, primary_key=True)
    Fuid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'), nullable=False)
    Ftype = Column(Integer, nullable=False, default=0)   # 1为约拍，2为  3-动态
    Ftypeid = Column(Integer, nullable=False, default=0)
    FT = Column(DateTime(timezone=True), default=func.now())
    Fvalid = Column(Boolean, nullable=False, default=1)

class AppointLike(Base):
    __tablename__ = 'AppointLike'

    ALid = Column(Integer,primary_key=True)
    ALapid = Column(Integer,ForeignKey('Appointment.APid',onupdate='CASCADE'))
    ALuid = Column(Integer,ForeignKey('User.Uid', onupdate='CASCADE'))
    ALvalid = Column(Boolean,nullable=False, default=1)
    ALT = Column(DateTime(timezone=True), default=func.now())

class Trend(Base):
    __tablename__ = "Trend"

    Tid = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    Tsponsorid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))  # 用户id
    Tsponsorimg = Column(VARCHAR(128), nullable=False)                                          # 用户头像
    Tualais = Column(VARCHAR(24), ForeignKey('User.Ualais', onupdate='CASCADE'), nullable=False)# 新增
    TsponsT = Column(DateTime(timezone=True), default=func.now())                               # 时间
    TcommentN = Column(Integer,nullable=False, default=0)                                       # 评论数
    TlikeN =Column(Integer,nullable=False, default=0)                                           # 点赞数
    Tcontent = Column(VARCHAR(128), nullable=False, default='')                                             # 动态内容
    Ttitle = Column(VARCHAR(12), nullable=False, default='')
    Tvalid = Column(Boolean, nullable=False, default=1)

class TrendComment(Base):  #动态评论
    __tablename__= "TrendComment"

    TRcmtid = Column(Integer, primary_key=True , nullable=False, autoincrement=True)
    TRcmttid = Column(Integer, ForeignKey('Trend.Tid', onupdate='CASCADE'))     #社区问题问题id
    TRcmtcontent = Column(VARCHAR(128), nullable=False)
    TRcmtT = Column(DateTime(timezone=True), default=func.now())
    TRcmtvalid = Column(Boolean, nullable=False, default=1)

class RankScore(Base):
    '''
       摄影师模特排行榜
       每个用户仅能有一列
       @RSMscore:用户在当模特方面的分数
       @RSPscore：用户在当摄影师方面的分数
    '''
    __tablename__ = 'RankScore'
    RSid = Column(Integer, nullable=False, primary_key=True)
    RSuid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'), nullable=False)
    RSMscore = Column(Integer, nullable=False, default=0)
    RSPscore = Column(Integer, nullable=False, default=0)
    RSMrank = Column(Integer, nullable=False, default=101)
    RSPrank = Column(Integer, nullable=False, default=101)


class UserCollection(Base): #用户作品集
    __tablename__ = 'UserCollection'

    UCid = Column(Integer, primary_key=True,nullable=False)
    UCuid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'),nullable=False)
    UCcreateT = Column(DateTime(timezone=True), default=func.now())
    #UCtitle = Column(VARCHAR(32), nullable=False)   # 作品集名称
    #UCcontent = Column(VARCHAR(128))                # 作品集描述
    UCvalid = Column(Integer, default=1)
    UCiscollection = Column(Integer, default=0)     # 0-作品集 1-个人照片
    UClikeN = Column(Integer, default=0)
    #UCcommentN = Column(Integer, default=0)
    UCuimurl = Column(VARCHAR(128), nullable=False)
    UCualais = Column(VARCHAR(24), ForeignKey('User.Ualais', onupdate='CASCADE'), nullable=False)  # 新增

class UserCollectionimg(Base):
    __tablename__ = 'UserCollectionimg'

    UCIuser = Column(Integer, ForeignKey(UserCollection.UCid, onupdate='CASCADE')) # 作品集id
    UCIimid = Column(Integer, ForeignKey(Image.IMid, onupdate='CASCADE'), primary_key=True)
    UCIurl = Column(VARCHAR(128))
    UCIvalid = Column(Integer, nullable=False, default=1)
    UCIheight = Column(Integer, default=0)
    UCIwidth = Column(Integer, default=0)

class UCollectlike(Base):
    __tablename__ = 'UCollectlike'

    UCLid = Column(Integer, primary_key=True)
    UCoLid = Column(Integer, ForeignKey(UserCollection.UCid, onupdate='CASCADE'))  #作品集id
    UCLUid = Column(Integer, ForeignKey(User.Uid, onupdate='CASCADE'))
    UCLvalid = Column(Boolean, nullable=False, default=1)
    UCLTime = Column(DateTime(timezone=True), default=func.now())

class UCcomment(Base):
    __tablename__ = 'UCcomment'

    UCcmtid = Column(Integer, primary_key=True)
    UCcmtcollid = Column(Integer, ForeignKey(UserCollection.UCid, onupdate='CASCADE'))
    UCcmtuid = Column(Integer, ForeignKey(User.Uid, onupdate='CASCADE'))
    UCcmtcontent = Column(VARCHAR(128))
    UCcmtvalid = Column(Boolean, nullable=False, default=1)
    UCcmtT = Column(DateTime(timezone=True), default=func.now())

class ApCompanion(Base):    #约拍伴侣
    __tablename__ = 'ApCompanion'

    ApCpnid=Column(Integer, primary_key=True)
    ApCpntitle = Column(VARCHAR(128))
    ApCpncontent = Column(VARCHAR(128))
    ApCpnValid = Column(Integer, nullable=False, default=1)
    ApCpnurl = Column(VARCHAR(128))

class CompanionImg(Base):
    __tablename__ = 'CompanionImg'

    Cpnimid = Column(Integer, primary_key=True)
    Cpnid = Column(Integer,ForeignKey(ApCompanion.ApCpnid, onupdate='CASCADE'))
    Cpnimgurl = Column(VARCHAR(128))
    CpnimgValid = Column(Integer, nullable=False, default=1)


class WApCompanions(Base):
    '''
    @author:黄鑫晨
    @name:约拍伴侣表
    '''
    __tablename__ = 'WApCompanions'
    WAPCid = Column(Integer, primary_key=True)
    WAPCname = Column(VARCHAR(64), nullable=False)   # 约拍伴侣名
    WAPCOrganintro = Column(VARCHAR(128), nullable=False)  # 组织/个人介绍
    WAPCServeintro = Column(VARCHAR(256), nullable=False)  # 提供服务介绍
    WAPCContact = Column(VARCHAR(128), nullable=False)  # 联系方式
    WAPCvalid = Column(Boolean, default=1, nullable=False)

class WApCompanionImage(Base):
    '''
    @author:黄鑫晨
    @name:约拍伴侣图片表
    '''
    __tablename__ = "WApCompanionImage"

    WAPCid = Column(Integer, ForeignKey('WApCompanions.WAPCid', onupdate='CASCADE'))
    WAPCimid = Column(Integer, primary_key=True)
    WAPCurl = Column(VARCHAR(128))  # 约拍伴侣图片链接
    WAPCvalid = Column(Boolean, default=1, nullable=False)


class WAcAuth(Base):    # 记录约拍伴侣发布码
    __tablename__ = 'WAcAuth'

    WAAid = Column(Integer, primary_key=True)
    WAauth = Column(VARCHAR(32), nullable=False)
    WAAacid = Column(Integer, ForeignKey('WApCompanions.WAPCid', onupdate='CASCADE'))  # 伴侣ID
    WAAused = Column(Boolean, nullable=False, default=0)  # 为0则未用， 1则用过


class Activity(Base):#活动表
    __tablename__ = 'Activity'

    ACid = Column(Integer,nullable=False, primary_key=True)
    ACsponsorid = Column(Integer,ForeignKey('User.Uid', onupdate='CASCADE'))  #活动发起者
    AClocation = Column(VARCHAR(128), nullable=False)
    ACtitle = Column(VARCHAR(24), nullable=False) # 活动的名称？确认长度
    ACtag = Column(VARCHAR(12)) # 活动的标签？确认类型
    ACstartT = Column(DateTime, nullable=False)
    ACendT = Column(DateTime, nullable=False)
    ACjoinT = Column(DateTime) # 活动报名截止时间
    ACcontent = Column(VARCHAR(128), nullable=False) # 活动介绍
    ACfree = Column(Boolean)
    ACprice = Column(VARCHAR(64))
    ACclosed = Column(Boolean,default=1, nullable=False) # 活动是否已经结束
    ACcreateT = Column(DateTime(timezone=True), default=func.now())
    ACcommentnumber = Column(Integer,default=0, nullable=False)
    ACmaxp = Column(Integer,nullable=False,default=0)
    ACminp = Column(Integer,nullable=False,default=100)
    ACscore = Column(Integer,nullable=False,default=0)
    AClikenumber = Column(Integer,nullable=False,default=0)
    ACvalid = Column(Boolean,nullable=False,default=1) # 活动是否已经删除
    ACregistN = Column(Integer,nullable=False,default=0)
    ACstatus =Column(Integer,nullable=False,default=0)

class ActivityEntry(Base):  #活动报名表
    __tablename__ = 'Activityaentry'

    ACEid=Column(Integer,primary_key=True)
    ACEacid = Column(Integer,ForeignKey('Activity.ACid',onupdate='CASCADE'))  # 活动ID
    ACEregisterid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'))  # 报名人ID
    ACEregisttvilid = Column(Boolean,default=1)
    ACEscore = Column(Integer,nullable=False,default=0)
    ACEcomment = Column(VARCHAR(128),nullable=False,default='')
    ACEregisterT = Column(DateTime(timezone=True), default=func.now())

class ActivityLike(Base):
    __tablename__ = 'ActivityLike'

    ACLid=Column(Integer,primary_key=True)
    ACLacid = Column(Integer,ForeignKey('Activity.ACid',onupdate='CASCADE'))
    ACLuid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'))
    ACLvalid = Column(Boolean,nullable=False,default=1)
    ACLT = Column(DateTime, default=func.now())



