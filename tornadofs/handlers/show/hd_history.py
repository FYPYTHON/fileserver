#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/17 13:37
# @Author  : 1823218990@qq.com
# @File    : hd_history.py
# @Software: PyCharm

import os
from io import StringIO, BytesIO
import base64
from tornado.web import authenticated
from PIL import Image
from urllib import parse
import json

from handlers.author.hd_main import get_disk_usage
from handlers.basehd import BaseHandler, check_authenticated
from tornado.log import app_log as weblog
from common.global_func import get_user_info, get_history_all, cal_page_from_total
import platform


class HistoryHandler(BaseHandler):
    @check_authenticated
    def get(self):
        curpath = self.get_argument('curpath', None)
        curpage = int(self.get_argument("page", "0"))
        if curpage <= 0:
            curpage = 1
        if curpath is None:
            curpath = 'public'
        offset = (curpage - 1) * 50
        historylist, count = get_history_all(self, offset)
        weblog.info("history page:{} total:{}".format(len(historylist), count))
        pages = cal_page_from_total(count)
        if curpage > pages: curpage = pages
        userinfo = get_user_info(self)
        self.render("history.html", historys=historylist, userinfo=userinfo, curpath=curpath,
                    useage=get_disk_usage(self, curpath), page=curpage, total=pages)

    @check_authenticated
    def post(self):
        curpage = int(self.get_argument("page", "0"))
        curpath = self.get_argument('curpath', None)
        offset = curpage * 50
        historylist, count = get_history_all(self, offset)
        # print(len(historylist))
        userinfo = get_user_info(self)
        self.render("history.html", historys=historylist, userinfo=userinfo, curpath=curpath,
                    useage=get_disk_usage(self, curpath), page=curpage, total=count)
