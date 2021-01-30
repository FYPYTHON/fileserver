# coding=utf-8
"""
created: 12/13
"""
import base64
import os
from io import BytesIO
import cv2
from PIL import Image
from psutil import disk_usage
from common.msg_def import IMAGE_SUFFIX, PAGESIZE
from handlers.basehd import BaseHandler, check_token, check_authenticated
from tornado.log import app_log as weblog
from common.global_func import get_user_info
import json

short_cut_size = (25, 25)


def get_disk_usage(self, path):
    if not path.startswith("/opt/data"):
        path = os.path.join(os.path.join(self.settings.get('top_path'), path))
    if not os.path.exists(path):
        return u"路径不存在"
    use_info = disk_usage(path)
    total = round(use_info.total / 1024 / 1024 / 1024, 2)
    # used = round(use_info.used / 1024 / 1024 / 1024, 2)
    free = round(use_info.free / 1024 / 1024 / 1024, 2)
    output = u"已用{} %, 可用{} / 共{} G".format(use_info.percent, free, total)
    return output


def get_imgshortcut_base64(realpath, suffix):
    if suffix == "jpg":
        suffix = "jpeg"
    img = Image.open(realpath)
    # img_size = os.path.getsize(realpath)
    # img = img.resize(short_cut_size, Image.ANTIALIAS)
    img.thumbnail(short_cut_size)
    # weblog.info("image wh: {} realpath:{}".format(img.size, realpath))
    output_buffer = BytesIO()
    img.save(output_buffer, format=suffix)
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data).decode()
    prefix = "data:image/gif;base64,"
    return prefix + base64_data


def get_videoshortcut_base64(realpath, suffix="jpeg"):

    cap = cv2.VideoCapture(realpath)
    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret, frame = False, None
    cap.release()
    img = Image.fromarray(frame)
    if ret:
        img.thumbnail(short_cut_size)
        output_buffer = BytesIO()
        img.save(output_buffer, format=suffix)

        weblog.info("video wh:{} realpath:{}".format(img.size, realpath))
        binary_data = output_buffer.getvalue()
        base64_data = base64.b64encode(binary_data).decode()

        # img.save("E:\\test2.jpg")
        prefix = "data:image/gif;base64,"

        return prefix + base64_data
    else:
        return None


def get_paths_app(file_path):
    # file_path = os.path.join('/opt/data', file_path)
    if "\\" in file_path:
        curpath = file_path.replace("\\", "/")
    dir_list = list()
    file_list = list()
    shortcut_list = list()
    if os.path.exists(file_path):
        content = sorted(os.listdir(file_path))
    else:
        content = list()
    for name in content:
        all_name = os.path.join(file_path, name)
        if os.path.isdir(all_name):
            if name not in dir_list:
                dir_list.append(name)
        elif os.path.isfile(all_name):
            if name not in file_list:
                file_list.append(name)
                # suffix = all_name.split(".")[-1]
                # if suffix in ["mp4"]:
                #     shortcut_list.append(get_videoshortcut_base64(all_name, "jpeg"))
                # elif suffix in IMAGE_SUFFIX:
                #     shortcut_list.append(get_imgshortcut_base64(all_name, suffix))
                # else:
                #     shortcut_list.append(None)

    dir_list.sort()
    # file_list.sort()
    return dir_list, file_list, shortcut_list


def get_paths(file_path, index=1):

    if "\\" in file_path:
        curpath = file_path.replace("\\", "/")
    dir_list = list()
    file_list = list()
    shortcut_list = list()
    if os.path.exists(file_path):
        content = sorted(os.listdir(file_path))
    else:
        content = list()
    index = index - 1
    total = len(content) // PAGESIZE if len(content) % PAGESIZE == 0 else len(content) // PAGESIZE + 1

    if len(content) >= index * PAGESIZE:
        endsize = (index + 1) * PAGESIZE if (index + 1) * PAGESIZE < len(content) else len(content)
        content = content[index * PAGESIZE: endsize]

    for name in content:

        all_name = os.path.join(file_path, name)
        if os.path.isdir(all_name):
            if name not in dir_list:
                dir_list.append(name)
        elif os.path.isfile(all_name):
            if name not in file_list:
                file_list.append(name)

                suffix = all_name.split(".")[-1]
                if suffix in ["mp4"]:
                    shortcut_list.append(get_videoshortcut_base64(all_name, "jpeg"))
                elif suffix in IMAGE_SUFFIX:
                    shortcut_list.append(get_imgshortcut_base64(all_name, suffix))
                else:
                    shortcut_list.append(None)
    # dir_list.sort()
    return dir_list, file_list, shortcut_list, total


class FSMainHandler(BaseHandler):

    # @authenticated
    @check_authenticated
    def get(self):
        curpath = self.get_argument("curpath", None)
        action = self.get_argument("action", None)
        curpage = int(self.get_argument("page", '1'))
        # curpath = unquote_plus(curpath)
        if action is not None and action != "APP":
            curpath = os.path.dirname(curpath)
        # print("curpath:", curpath)
        userinfo = get_user_info(self)
        # upload_path = self.settings.get('upload_path')
        # if curpath is None or curpath == "" or curpath == "/":
        #     curpath = os.path.basename(upload_path)

        # new 20200821
        total = 1
        if curpage < 1:
            curpage = 1
        if curpath is not None and curpath.startswith("/"):
            curpath = curpath[1:]
        if curpath is None or curpath == "" or curpath == "/":
            # curpath = os.path.basename(upload_path)
            curpath = ""
            dir_list = ["public", "private"]
            file_list = []
            shortcut_list = []
        elif curpath.startswith("private"):
            private_path = os.path.join(self.top_path, "private", self.current_user)
            if not os.path.exists(private_path):
                os.makedirs(private_path)
            # private_curpath = curpath[0:7] + "/" + self.current_user + curpath[7:]
            if curpath == "private":
                dir_list = [self.current_user]
                file_list = []
                shortcut_list = []
            else:
                real_path = os.path.join(self.top_path, curpath)
                dir_list, file_list, shortcut_list, total = get_paths(real_path, curpage)
        else:
            real_path = os.path.join(self.top_path, curpath)
            dir_list, file_list, shortcut_list, total = get_paths(real_path, curpage)

        # real_path = os.path.join(self.top_path, curpath)
        # dir_list, file_list, shortcut_list = get_paths(real_path)
        if curpage > total:
            curpage = total
        weblog.info("page:{}/{}".format(curpage, total))
        return self.render("fsmain.html", userinfo=userinfo, curpath=curpath, dirs=dir_list, files=file_list,
                           shortcut_list=shortcut_list, useage=get_disk_usage(self, curpath), page=curpage, total=total)

    @check_authenticated
    def post(self):
        pass

    def delete(self):
        pass


class AppFSMainHandler(BaseHandler):

    @check_token
    def get(self):
        curpath = self.get_argument("curpath", None)
        action = self.get_argument("action", None)
        loginname = self.get_argument("loginname", None)
        # curpath = unquote_plus(curpath)
        if loginname is None:
            return self.write(json.dumps({"error_code": 1, "msg": u"用户未登陆"}))
        if action is not None:
            curpath = os.path.dirname(curpath)
        # print("curpath:", curpath)

        # userinfo = get_user_info(self)
        # upload_path = self.settings.get('upload_path')
        # if curpath is None or curpath == "" or curpath == "/":
        #     curpath = os.path.basename(upload_path)
        #
        # real_path = os.path.join(self.top_path, curpath)
        # dir_list, file_list, shortcut_list = get_paths_app(real_path)

        # new 20200821
        if curpath is not None and curpath.startswith("/"):
            curpath = curpath[1:]
        if curpath is None or curpath == "" or curpath == "/":
            # curpath = os.path.basename(upload_path)
            curpath = ""
            dir_list = ["public", "private"]
            file_list = []
            shortcut_list = []
        elif curpath.startswith("private"):
            private_path = os.path.join(self.top_path, "private", loginname)
            if not os.path.exists(private_path):
                os.makedirs(private_path)
            # private_curpath = curpath[0:7] + "/" + self.current_user + curpath[7:]
            if curpath == "private":
                dir_list = [loginname]
                file_list = []
                shortcut_list = []
            else:
                real_path = os.path.join(self.top_path, curpath)
                dir_list, file_list, shortcut_list = get_paths_app(real_path)
        else:
            real_path = os.path.join(self.top_path, curpath)
            dir_list, file_list, shortcut_list = get_paths_app(real_path)

        return self.write(json.dumps({"error_code": 0, "dirs": dir_list, "files": file_list,
                                      "curpath": curpath, "shortcut_list": shortcut_list,
                                      "useage": get_disk_usage(self, curpath)}))
