# coding=utf-8
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
from handlers.basehd import BaseHandler, check_authenticated, check_token
from common.global_func import get_user_info


class FsCreateHandler(BaseHandler):
    @check_authenticated
    def post(self):
        newname = self.get_argument("newname", None)
        curpath = self.get_argument("curpath", None)

        # print(newname, curpath)
        toppath = self.settings.get("top_path")

        real_newname = os.path.join(toppath, curpath, newname)

        if os.path.exists(real_newname):
            return self.write(json.dumps({"msg": "{} is exist".format(newname), "code": 1}))

        if curpath == "private":
            return self.write(json.dumps({"msg": "{} directory can not create new".format(newname), "code": 1}))

        try:
            # os.mkdir(real_newname)
            os.makedirs(real_newname)
            return self.write(json.dumps({"msg": "ok", "code": 0}))
        except Exception as e:
            weblog.exception(e)
            return self.write(json.dumps({"msg": "create dir error", "code": 1}))


class AppFsCreateHandler(BaseHandler):
    @check_token
    def post(self):
        newname = self.get_argument("newname", None)
        curpath = self.get_argument("curpath", None)

        # print(newname, curpath)
        toppath = self.settings.get("top_path")

        real_newname = os.path.join(toppath, curpath, newname)

        if os.path.exists(real_newname):
            return self.write(json.dumps({"msg": u"目录已存在".format(newname), "error_code": 1}))

        if curpath == "private":
            return self.write(json.dumps({"msg": "当前目录下不能创建新目录".format(newname), "code": 1}))

        try:
            # os.mkdir(real_newname)
            os.makedirs(real_newname)
            return self.write(json.dumps({"msg": u"创建成功", "error_code": 0}))
        except Exception as e:
            weblog.exception(e)
            return self.write(json.dumps({"msg": u"创建失败", "error_code": 1}))