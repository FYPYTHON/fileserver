#!/usr/bin/env python
# coding=utf-8

import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.tbl_code import TblCode


def clear_db():

    engine = create_engine('sqlite:///wfs.db?check_same_thread=False', echo=True)
    Session = sessionmaker(bind=engine)
    db_session = Session()

    print("drop database....")
    # db_session.execute('drop database if EXISTS weekpost;')
    # db_session.execute('create database weekpost default charset utf8 collate utf8_general_ci;')


def create_table():

    import os.path
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk("./database"):
        root = root.strip(".%s" % os.path.sep)
        for f in files:
            if f.startswith("tbl_") and f.endswith(".py"):
                py_module = os.path.join(root, f[:-3]).replace(os.path.sep, ".")

                cmd = "import %s" % py_module
                print(cmd,py_module,f[:-3])
                exec(cmd)

    from database import db_config

    print ("drop table....")
    db_config.ModelBase.metadata.drop_all(db_config.engine)

    print ("create table....")
    db_config.ModelBase.metadata.create_all(db_config.engine)

    print ("done!")


def get_table_propery(name=None):
    from database.db_config import engine, ModelBase
    ModelBase.metadata.reflect(engine)
    tables = ModelBase.metadata.tables
    for tbl, value in tables.items():
        if name is None:
            print(tbl, value.__repr__())
        else:
            if name == tbl:
                print(tbl, value.__repr__())

def create_single_table():
    # from database import tbl_bug_list
    # from database import tbl_bug_track
    # from database import tbl_topic
    # from database import tbl_account
    # from database import tbl_version
    # from database import tbl_account
    # from database import tbl_browsing_history
    # from database import tbl_jijin
    # from database import tbl_admin
    # from database import tbl_poetry
    # from database import tbl_word
    # from database import tbl_code
    from database import tbl_sum
    from database import db_config
    print("create table....")
    db_config.ModelBase.metadata.create_all(db_config.engine)


def init_data():
    print('init_data...')
    from database.db_config import db_session
    from database.tbl_admin import TblAdmin
    user = TblAdmin()
    user.name = "__MAIL__"
    user.value = "1823218990@qq.com"
    user.type = 1
    email = TblAdmin()
    email.name = "__MAILPASSWORD__"
    email.value = "xxxxxxxxxx"
    email.type = 1
    user_exist = db_session.query(TblAdmin.name).filter(TblAdmin.name == user.name).first()
    if user_exist is None:
        db_session.add(user)

    mail_exist = db_session.query(TblAdmin.name).filter(TblAdmin.name == email.name).first()
    if mail_exist is None:
        db_session.add(email)
    db_session.commit()
    db_session.close()



def init_account():
    print('init one account...')
    from database.db_config import db_session
    from database.tbl_account import TblAccount
    from method.data_encode import MD5
    account = TblAccount()
    account.loginname = "Tornado"
    account.nickname = u"飞影"
    account.password = MD5("邓艾郭嘉")
    account.userrole = 0
    account.userstate = 0
    account.email = "1823218990@qq.com"
    db_session.add(account)
    db_session.commit()
    db_session.close()
    print("add ok")


if __name__ == '__main__':
    # clear_db()
    # create_table()
    # init_account()
    # init_data()
    create_single_table()
    # from database.db_config import db_session
    # db_session.commit()
    #
    # get_table_propery("tbl_word")
    # # init_account()
    #
    # db_session.add(TblCode(key="admin1", msg=1, code='4K6h3JXgrLXgu43jkKPjiZnjjL', user="admin1"))
    # db_session.commit()
    # all_code = db_session.query(TblCode).filter(TblCode.user == "admin1").all()
    # for i in all_code:
    #     print(i.tojson())







