#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/4 13:25
# @Author  : 1823218990@qq.com
# @File    : tbl_code.py
# @Software: PyCharm


from sqlalchemy import Column, String, Integer, UniqueConstraint, Index
from database import table_base
from database.db_config import ModelBase


class TblCode(ModelBase, table_base.TableBase):
    __tablename__ = 'tbl_code'

    id = Column(Integer, unique=True, primary_key=True)
    code = Column(String(100), comment=u"密文")
    msg = Column(String(200), comment=u"描述")
    key = Column(String(50), comment=u"关键字")
    user = Column(String(50), comment=u"归属")

    __table_args__ = (
        UniqueConstraint('user', 'key', name='user_key'),
        Index('ix_id_user_key', 'id', 'user', key),
    )


    def tojson(self):
        return {
            "id": self.id,
            "code": self.code,
            "msg": self.msg,
            "key": self.key,
            "user": self.user
        }

    def __repr__(self):
        return "%s<id=%s, key=%s,code=%s>" % (self.__class__.__name__, self.id, self.key, self.code)