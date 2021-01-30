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
from handlers.basehd import BaseHandler, check_token, check_authenticated
from common.global_func import get_user_info
from tornado.log import app_log as weblog


class FsRenameHandler(BaseHandler):
    # @authenticated
    @check_authenticated
    def post(self):
        oldname = self.get_argument("oldname", None)
        newname = self.get_argument("newname", None)
        curpath = self.get_argument("curpath", None)


        toppath = self.settings.get("top_path")
        real_oldname = os.path.join(toppath, curpath, oldname)
        real_newname = os.path.join(toppath, curpath, newname)
        if not os.path.exists(real_oldname):
            return self.write(json.dumps({"msg": "orignal file is miss", "code": 1}))
        if os.path.exists(real_newname):
            return self.write(json.dumps({"msg": "{} is exist".format(newname), "code": 1}))

        try:
            os.rename(real_oldname, real_newname)
            return self.write(json.dumps({"msg": "ok", "code": 0}))
        except Exception as e:
            weblog.exception(e)
            return self.write(json.dumps({"msg": "rename error", "code": 1}))


class AppFsRenameHandler(BaseHandler):
    @check_token
    def post(self):
        oldname = self.get_argument("oldname", None)
        newname = self.get_argument("newname", None)
        curpath = self.get_argument("curpath", None)

        weblog.info("{} {} {} ".format(oldname, newname, curpath))
        toppath = self.settings.get("top_path")
        real_oldname = os.path.join(toppath, curpath, oldname)
        real_newname = os.path.join(toppath, curpath, newname)
        if not os.path.exists(real_oldname):
            return self.write(json.dumps({"msg": u"原始文件不存在", "error_code": 1}))
        if os.path.exists(real_newname):
            return self.write(json.dumps({"msg": u"{}已存在".format(newname), "error_code": 1}))

        try:
            os.rename(real_oldname, real_newname)
            return self.write(json.dumps({"msg": u"重命名成功", "error_code": 0}))
        except Exception as e:
            weblog.exception(e)
            return self.write(json.dumps({"msg": u"重命名失败", "error_code": 1}))