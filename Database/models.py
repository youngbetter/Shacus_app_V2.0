# -*- coding: utf-8 -*-
import sys
import redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
'''
@author: 黄鑫晨
'''
reload(sys)
# python的str默认是ascii编码，和unicode编码冲突,需处理
sys.setdefaultencoding('utf8')
#数据库地址
DB_CONNECT_STRING = 'mysql+mysqldb://root:ydrs.sql.7234@123.206.227.249:3306/SHACUS_APP_V2?charset=utf8'

#测试数据库地址
#DB_CONNECT_STRING = 'mysql+mysqldb://root@127.0.0.1:3307/shacustest?charset=utf8'
#DB_CONNECT_STRING = 'mysql+mysqldb://root@127.0.0.1/shacus_app?charset=utf8'

#redis缓存
#pool = redis.ConnectionPool(host='123.206.227.249', port=32798,password='ydrs.redis.7234')

pool = redis.ConnectionPool(host='127.0.0.1', port=800,password='ydrs.redis.7234')
redis_engine = redis.Redis(connection_pool=pool)


#  pool_recycle=10
# 返回数据库引擎，即连接数据库
engine = create_engine(DB_CONNECT_STRING, echo=False, pool_size=100, max_overflow=300)
connection = engine.connect()

# declarative_base() 创建了一个 BaseModel 类，这个类的子类可以自动与一个表关联。
Base = declarative_base()
# Construct a base class for declarative class definitions.

if(engine!=None):
    print "数据库连接成功，return"+str(connection)
    Base.metadata.create_all(engine)

else:
    print "数据库连接失败"

db2 = None
def get_db():
    '''
    Returns:返回数据库操作session
    '''
    global db2
    #if not db:
    db2 = scoped_session(sessionmaker(bind=engine,
                                         autocommit=False, autoflush=True,
                                         expire_on_commit=False))
    return db2

