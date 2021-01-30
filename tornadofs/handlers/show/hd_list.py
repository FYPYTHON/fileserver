# coding=utf-8
"""
created: 2020/1/18
"""
import os
from io import StringIO, BytesIO
import base64
from tornado.web import authenticated
from PIL import Image
import json
from handlers.basehd import BaseHandler
from tornado.log import app_log as weblog
from common.global_func import get_user_info
import platform


class FsListHandler(BaseHandler):
    def get(self):
        ftype = self.get_argument("type", None)
        curpath = self.get_argument("curpath", None)
        pass

    @staticmethod
    def get_flist(file_path, ftype):
        file_path = os.path.join('/opt/data', file_path)
        if "\\" in file_path:
            file_path = file_path.replace("\\", "/")
        file_list = list()
        if os.path.exists(file_path):
            content = os.listdir(file_path)
        else:
            content = list()
        for name in content:
            all_name = os.path.join(file_path, name)
            if os.path.isfile(all_name):
                subfix = os.path.splitext(all_name)
                if ftype == 'img':
                    if subfix not in ["png", 'jpg', 'jpeg', 'gif']:
                        continue
                else:
                    if subfix not in ['mp4']:
                        continue
                if name not in file_list:
                    file_list.append(name)
        file_list.sort()
        return file_list