#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 15:10
# @Author  : 1823218990@qq.com
# @File    : mysql_config.py
# @Software: PyCharm

from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, Text
from sqlalchemy.orm import sessionmaker, scoped_session, deferred
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import pymysql
pymysql.install_as_MySQLdb()

ModelBase = declarative_base()

# host = "172.16.83.226"

# port = 3306
host = "192.168.0.223"
port = 3360

# postgresql+psycopg2://user:password@hostname:port/database_name
engine = create_engine('mysql://root:fy123456@{}:{}/testonly?charset=utf8'.format(host, port), echo=False)
session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)


class TblAdmin(ModelBase):
    __tablename__ = 'tbl_admin_modb'

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(60), unique=True, comment=u"变量名")
    value = Column(String(60))
    type = Column(Integer)

    def __repr__(self):
        return "%s<id=%s, name=%s,value=%s,type=%s>" % (self.__class__.__name__, self.id, self.name, self.value, self.type)
ModelBase.metadata.create_all(engine)


def get_randstr(num):
    import random
    str = ''
    for i in range(num):
        str += random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
    return str

def add_data():
    from datetime import datetime
    id = db_session.query(TblAdmin).order_by(TblAdmin.id.desc()).limit(1).first()
    for i in range(2000):
        dd = TblAdmin()
        dd.name = get_randstr(10)
        dd.value = get_randstr(5)
        dd.type = i % 5
        print(dd, datetime.now(), id.id + i)
        db_session.add(dd)
        db_session.commit()
        import time
        time.sleep(0.1)


def search():
    a = db_session.query(TblAdmin).order_by(TblAdmin.id.desc()).limit(2).all()
    for i in a:
        print(i)


if __name__ == '__main__':
    pass
    add_data()
    search()

