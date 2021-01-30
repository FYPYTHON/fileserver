#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/11 10:58
# @Author  : 1823218990@qq.cmo
# @File    : hd_dbinfo.py
# @Software: PyCharm

from handlers.basehd import BaseHandler, check_token
from database.tbl_poetry import TblPoetry
from database.tbl_alticle import TblAlticle
from database.tbl_browsing_history import TblBrowsingHistory
from database.tbl_jijin import TblJijin
import json


class DbinfoHandler(BaseHandler):
    @check_token
    def get(self):
        poem_count = self.mysqldb().query(TblPoetry).count()
        alticle_count = self.mysqldb().query(TblAlticle).count()
        history_count = self.mysqldb().query(TblBrowsingHistory).count()
        jijin_count = self.mysqldb().query(TblJijin).count()
        return self.write(json.dumps({"poem": poem_count,
                                      "alticle": alticle_count,
                                      "history": history_count,
                                      "jijin": jijin_count}))

