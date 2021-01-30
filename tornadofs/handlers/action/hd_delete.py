#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/24 15:20
# @Author  : 1823218990@qq.com
# @File    : hd_delete.py.py
# @Software: PyCharm

import os
import json
from tornado.log import app_log as weblog
from handlers.basehd import BaseHandler, check_authenticated, check_token


class FsDeleteHandler(BaseHandler):
    @check_authenticated
    def delete(self):
        curpath = self.get_argument("curpath", None)
        filelist = self.get_arguments("filelist[]", False)  # super subor
        if curpath is not None and curpath.startswith("public/File") and self.get_current_user() != "Tornado":
            weblog.info("{} can not delete".format(curpath))
            return self.write(json.dumps({"error_code": 1, "msg": u"该目录下的文件不能删除"}))
        # print(self.request.arguments)
        # print(self.get_query_arguments("filelist"))
        for i in range(len(filelist)):
            file = filelist[i]
            real_file = os.path.join(self.settings.get("top_path"), file)
            filelist[i] = real_file
            if not os.path.exists(real_file):
                msg = u"{}不存在".format(file)
                return self.write(json.dumps({"error_code": 1, "msg": msg}))

        file_str = " ".join(filelist)
        try:
            # cmd = "rm -rf {}".format(file_str)
            cmd = "mv {} /home/trash".format(file_str)
            weblog.info("{}".format(cmd))
            os.system(cmd)
            return self.write(json.dumps({"error_code": 0, "msg": "文件已删除"}))
        except Exception as e:
            weblog.exception("{}".format(e))
            return self.write(json.dumps({"error_code": 1, "msg": u"删除失败"}))

    @check_token
    def post(self):
        pass


class AppFsDeleteHandler(BaseHandler):
    @check_token
    def post(self):
        curpath = self.get_argument("curpath", None)
        filename = self.get_argument("filename", None)  # super subor

        if curpath is None:
            return self.write(json.dumps({"error_code": 1, "msg": u"当前路径为空"}))
        else:
            real_file = os.path.join(self.settings.get("top_path"), curpath, filename)

        if curpath is not None and curpath.startswith("public/File"):
            weblog.info("{} can not delete".format(curpath))
            return self.write(json.dumps({"error_code": 1, "msg": u"该目录下的文件不能删除"}))

        if not os.path.exists(real_file):
            msg = u"{}不存在".format(real_file)
            return self.write(json.dumps({"error_code": 1, "msg": msg}))

        try:
            # cmd = "rm -rf {}".format(real_file)
            cmd = "mv {} /home/trash".format(real_file)
            weblog.info("{}".format(cmd))
            os.system(cmd)
            return self.write(json.dumps({"error_code": 0, "msg": "文件已删除"}))
        except Exception as e:
            weblog.exception("{}".format(e))
            return self.write(json.dumps({"error_code": 1, "msg": u"删除失败"}))
