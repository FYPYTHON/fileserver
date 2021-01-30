#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/13 16:53
# @Author  : 1823218990@qq.com
# @File    : hd_avator.py
# @Software: PyCharm

import os
import json
import platform
import tornado.web
import tornado.gen
from tornado.web import authenticated
import tornado.httpclient
from tornado.web import stream_request_body
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.log import app_log as weblog
from handlers.basehd import BaseHandler, check_token, check_authenticated
from common.global_func import get_user_info
from tornado.log import app_log as weblog


class FsAvatorHandler(BaseHandler):
    @check_token
    def post(self):
        loginname = self.get_argument("loginname")
        filepath = self.get_argument("avator_path")

        files = self.request.files['files']
        weblog.critical("{} {} ".format(loginname, filepath))
        # count = 0
        real_file = None
        suffix = "png"
        for fmeta in files:
            filesize = len(fmeta['body'])
            fname = fmeta['filename']
            suffix = fname.split(".")[-1]
            if suffix not in ["png", "jpg", 'jpeg']:
                return self.write(json.dumps({"error_code": 1, "msg": u"图片格式错误(只支持png, jpg, jpeg)".format(fname)}))
            if filesize > 1048576:
                return self.write(json.dumps({"error_code": 1, "msg": u"头像图片太大了（< 1M）".format(fname)}))
            weblog.info("{} {} {}M".format(filepath, fname, round(float(filesize * 1.0 / 1024 / 1024)), 2))
            real_file = os.path.join(self.settings.get("static_path"), "img/avator", fname)
            if os.path.exists(real_file):
                weblog.error(u"{} is exist".format(real_file))
                return self.write(json.dumps({"error_code": 1, "msg": u"上传失败，{} 已存在".format(fname)}))
            with open(real_file, 'wb') as up:  # os拼接文件保存路径，以字节码模式打开
                up.write(fmeta['body'])  # 将文件写入到保存路径目录

        if real_file is None:
            return self.write(json.dumps({"msg": u"文件不存在", "error_code": 1}))
        try:
            os.rename(real_file, os.path.join(self.settings.get("static_path"), "img/avator", loginname + "." + suffix))
        except Exception as e:
            weblog.error("{}".format(e))
            return self.write(json.dumps({"msg": u"头像上传失败", "error_code": 1}))
        return self.write(json.dumps({"msg": u"头像上传成功", "error_code": 0}))

