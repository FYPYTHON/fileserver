# coding=utf-8

from sqlalchemy import Column, String, Integer,DateTime
from datetime import datetime
from database import table_base
from database.db_config import ModelBase
"""
#
# 因为如果用varchar 来存储年月日，那么需要10个字节，而date类型只需4个字节，
# 而datetime类型也只需要8个字节，都小于varchar类型。
#
# 其次，在进行查找、比较时，由于date和datetime本质上存储在数据库中是一个数字，所以直接通过数值比较效率很高，而
# varchar进行比较 必需要一个字符一个字符比较，所以速度很慢。
#
# 如果再想深一点，一条记录少了几个字节，关键是如果记录数多，那么总体节省的字节数就会很多，另
# 外，加载到内存后，闸弄的内存更少，同时也只需要更少的IO，查询速度更快。
"""


class TblAccount(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_account'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    loginname = Column(String(100), unique=True, nullable=False)
    nickname = Column(String(20), default=u"Tornado", nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    userstate = Column(Integer, comment=u"0=正常，1=不可用", default=1)
    userrole = Column(Integer, comment=u"0=超管，1=管理, 2=普通, 3=临时", default=3)
    register_time = Column(DateTime, default=datetime.now())
    last_logintime = Column(DateTime, default=datetime.now())
    avatar_path = Column(String(100), comment=u"用户头像地址", default="")
    token = Column(String(100), comment=u"token", default="")

    def __repr__(self):
        return "%s<id=%s, loginname=%s,email=%s>" % (self.__class__.__name__, self.id, self.loginname, self.email)
