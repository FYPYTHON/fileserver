# coding=utf-8
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, Text
from sqlalchemy.orm import sessionmaker, scoped_session, deferred
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL


ModelBase = declarative_base()
host = '192.168.0.224'
# host = "172.16.83.227"
db = 'modb'
url = URL(drivername='postgresql+psycopg2', username='highgo', password='highgo123',
          host=host, database=db, port=5866)
engine = create_engine(url, echo=True)

# postgresql+psycopg2://user:password@hostname:port/database_name
# engine = create_engine('postgresql+psycopg2://highgo:highgo123@192.168.0.224:5866/ap', echo=True)
session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)


class TblAdmin(ModelBase):
    __tablename__ = 'tbl_admin_modb'

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(60), unique=True, comment=u"变量名")
    value = Column(String(60))
    type = Column(Integer)

    def __repr__(self):
        return "%s<id=%s, name=%s,value=%s>" % (self.__class__.__name__, self.id, self.name, self.value)
ModelBase.metadata.create_all(engine)

class TblBrowsingHistory(ModelBase):
    __tablename__ = 'tbl_browsing_history_modb'

    id = Column(Integer, unique=True, primary_key=True)
    user_ip = Column(String(100))         # 访问ip
    user_account = Column(String(100))    # 登录用户
    uri = Column(String(255))             # 访问地址

    request_method = Column(String(100))  # post/get
    status = Column(String(100))          # 访问状态码
    browsing_date = Column(String(20))   # 访问日期
    browsing_time = Column(String(20))    # 访问时间
    user_agent = Column(String(200))        # 用户代理

    def __repr__(self):
        return "%s<user_account=%s, user_ip=%s>" % (self.__class__.__name__, self.user_account, self.user_ip)
ModelBase.metadata.create_all(engine)
class TblWord(ModelBase):
    __tablename__ = 'tbl_word_modb'
    id = Column(Integer, unique=True, nullable=False, primary_key=True)
    word = Column(String(20), nullable=False, unique=True)
    chn = Column(String(20), default="")
    picture = deferred(Column(Text))
    suffix = Column(String(5), default="png")
    agg = Column(String(20), default=u"常用")
    describe = deferred(Column(Text))
ModelBase.metadata.create_all(engine)

def add_word():
    for i in range(10):
        wd = TblWord()
        wd.word = get_randstr(10)
        wd.chn = get_randstr(5)
        wd.picture = get_randstr(100)
        wd.suffix = get_randstr(4)
        wd.agg = get_randstr(20)
        wd.describe = get_randstr(200)
        db_session.add(wd)
        db_session.commit()

def add_data():
    from datetime import datetime
    for i in range(10):
        dd = TblAdmin()
        dd.name = get_randstr(10)
        dd.value = get_randstr(5)
        dd.type = i % 5
        db_session.add(dd)
        db_session.commit()


def get_randstr(num):
    import random
    str = ''
    for i in range(num):
        str += random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
    return str


def add_history():
    from datetime import datetime
    for i in range(10):
        hs = TblBrowsingHistory()
        hs.uri = "//" + get_randstr(5)
        hs.browsing_time = str(datetime.now())[0:19]
        hs.browsing_date = str(datetime.now().date())
        hs.status = 400
        hs.request_method = get_randstr(5)
        hs.user_account = get_randstr(5)
        hs.user_agent = get_randstr(5)
        hs.user_ip = "192.168.0." + str(i)
        db_session.add(hs)
        db_session.commit()


if __name__ == '__main__':
    for i in range(10000):
        add_data()
        add_history()
        add_word()
    db_session.close()
