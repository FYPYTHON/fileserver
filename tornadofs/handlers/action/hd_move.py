# coding=utf-8
import os
import json
from shutil import move
from tornado.web import authenticated
from tornado.log import app_log as weblog
from handlers.basehd import BaseHandler, check_authenticated, check_token
from handlers.author.hd_main import FSMainHandler, get_paths


class FsMoveHandler(BaseHandler):
    # @authenticated
    @check_authenticated
    def get(self):
        curpath = self.get_argument("curpath", None)
        action = self.get_argument("action", None)  # super subor
        if curpath is not None:
            newpath = curpath
            curpath = os.path.join(self.settings.get("top_path"), curpath)
            public_path = os.path.join(self.settings.get("top_path"), "public")
            if os.path.exists(curpath):
                # if os.path.isfile(curpath):
                if curpath == public_path:
                    pass
                else:
                    curpath = os.path.dirname(curpath)

                if action == "super":
                    if curpath != public_path:
                        curpath = os.path.dirname(curpath)
                        newpath = os.path.dirname(newpath)
                    else:
                        curpath = public_path
                        newpath = newpath

                if action == "subor":
                    curpath = os.path.join(self.settings.get("top_path"), newpath)
                    newpath = newpath

                dirlist = get_paths(curpath)[0]


                # else:
                #     dirlist = [os.path.join(curpath, dir).replace("\\", "/") for dir in dirlist]
                return self.write(json.dumps({"msg": "ok", "movepaths": dirlist, "code": 0, "newpath": newpath}))
        else:
            return self.write(json.dumps({"msg": u"当前路径不存在", "code": 1}))




    @check_authenticated
    def post(self):
        oldpath = self.get_argument("oldpath", None)
        newpath = self.get_argument("newpath", None)
        # curpath = self.get_argument("curpath", None)

        if not oldpath or not newpath:
            return self.write(json.dumps({"msg": u"文件或目录不存在", "code": 1}))
        toppath = self.settings.get("top_path")
        real_oldname = os.path.join(toppath, oldpath)
        real_newname = os.path.join(toppath, newpath)

        if not os.path.exists(real_oldname):
            return self.write(json.dumps({"msg": u"当前文件或目录不存在", "code": 1}))

        basename = os.path.basename(oldpath)
        move_path = os.path.join(real_newname, basename)

        if os.path.isdir(real_oldname) and os.path.exists(move_path):
            weblog.error("{}".format(move_path))
            return self.write(json.dumps({"msg": u"新目录已存在", "code": 1}))
            pass
        if not os.path.isdir(real_newname) and os.path.isfile(real_oldname):
            return self.write(json.dumps({"msg": u"新目录不存在".format(newpath), "code": 1}))

        try:
            weblog.info("move {} to {} ".format(real_oldname, real_newname))
            move(real_oldname, real_newname)
            return self.write(json.dumps({"msg": "ok", "code": 0}))
        except Exception as e:
            weblog.exception(e)
            return self.write(json.dumps({"msg": u"移动失败", "code": 1}))