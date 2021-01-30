# coding=utf-8
import hashlib
"""
    #from database.tbl_account import TblAccount
    #engine.execute("ALTER TABLE tbl_account ADD token char(100);")
    #engine.execute("select * from tbl_account;")
    from database.tbl_poetry import TblPoetry
    from database.tbl_alticle import TblAlticle
    
    # group by
    # res = db_session.query(func.count(TblAlticle.id), TblAlticle.agg).group_by(TblAlticle.agg).all()
    # print(len(res), 'agg')
    # for r in sorted(res):
    #     print(r)
    
    # like
    # te = db_session.query(TblPoetry.content, TblPoetry.id).filter(TblPoetry.content.like(u"北国风光%")).all()
    # te = db_session.query(TblPoetry).filter(TblPoetry.content.like(u"北国风光%")).all()
    # print(len(te))
    # for t in te:
    #     print(t.tojson())
    #     print(len(t.content))
    
    # func.min func.max func.avg
    from sqlalchemy import func
    from database.tbl_jijin import TblJijin
    tj = db_session.query(TblJijin.jid, TblJijin.jdate, func.min(TblJijin.jvalue)).filter(TblJijin.jid == '1717')
    for t in tj.all():
        print(t)
"""
from database.db_config import db_session, engine
from method.data_encode import MD5

def init_admin():
    from database.tbl_admin import TblAdmin
    user = TblAdmin()
    user.name = "appversion"
    user.value = "1.0"
    user.type = 1
    db_session.add(user)
    db_session.commit()
    db_session.close()

def init_version():

    from database.tbl_admin import TblAdmin
    version = TblAdmin()
    version.name = "appversion"
    version.value = "1.0"
    version.type = 1
    db_session.add(version)
    db_session.commit()
    db_session.close()

def init_user():
    from database.tbl_account import TblAccount
    account = TblAccount()
    account.loginname = "youth303"
    account.nickname = u"青春"
    account.password = MD5("303303")
    account.email = ""
    account.userstate = 0
    account.userrole = 2
    db_session.add(account)
    db_session.commit()
    db_session.close()

def init_setting():
    from database.tbl_admin import TblAdmin
    db_session.add_all([
    TblAdmin(name="currentname",value="feiying",type=0),
    TblAdmin(name="description",value="test only",type=0),
    TblAdmin(name="admin_email", value="1490726887@qq.com", type=0),
    TblAdmin(name="can_register", value="1", type=1),
    TblAdmin(name="can_comment", value="1", type=1),
    TblAdmin(name="comments_notify", value="1", type=1),
    TblAdmin(name="default_category", value="default_category", type=0),
    TblAdmin(name="page_size", value="10", type=1),
    TblAdmin(name="rss_size", value="10", type=1),
    TblAdmin(name="rss_excerpt", value="1", type=1),
    TblAdmin(name="new_rss_size", value="5", type=1),
    TblAdmin(name="new_page_size", value="5", type=1),
    ])

    db_session.commit()

def init_jijin():
    from database.tbl_jijin import TblJijin
    from datetime import datetime
    dis = TblJijin()
    dis.jid = "test2"
    dis.jdate = '2020-05-05'
    dis.jvalue = '2.13'
    db_session.add(dis)
    db_session.commit()


if __name__ == "__main__":
    # init_admin()
    # init_user()
    # init_setting()
    # init_version()
    from sqlalchemy import func
    from database.tbl_jijin import TblJijin
    tj = db_session.query(TblJijin.jid, TblJijin.jdate, func.min(TblJijin.jvalue)).filter(TblJijin.jid == '1717')
    for t in tj.all():
        print(t)

    # te = tj.delete()
    # db_session.commit()








