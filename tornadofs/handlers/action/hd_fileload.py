#!/usr/bin/env python
# encoding: utf-8
import os
import json
import platform
import tornado.web
import tornado.gen
from tornado.web import authenticated
import tornado.httpclient
from urllib import parse
from tornado.web import stream_request_body
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.log import app_log as weblog

from handlers.author.hd_main import get_disk_usage
from handlers.basehd import BaseHandler, check_token, check_authenticated
from common.global_func import get_user_info

time1 = 10
buf_size = 4096
MAX_SINGLE = 1024 * 1024 * 1024
MAX_STREAMED_SIZE = 1024 * 1024 * 1024
BASE_DIR = "/opt/data"


def urldecode_path(path):
    if isinstance(path, str):
        if '+' in path:
            return parse.unquote_plus(path)
        else:
            return parse.unquote(path)
    else:
        return path


def urlencode_path(path):
    if isinstance(path, str):
        if ' ' in path:
            return parse.quote_plus(path)
        else:
            return parse.quote(path)
    else:
        return path

class DownloadHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    # @check_authenticated
    # @authenticated
    @tornado.gen.coroutine
    def get(self):
        filename = self.get_argument('filename', None)
        # smd5 = self.get_argument('smd5', '0')
        # fsize = int(self.get_argument('fsize', '0'))   # 客户端文件大小
        if filename is None:
            return self.write(json.dumps({'msg': 'file is none.', 'code': 1}))
        filename = urldecode_path(filename)
        fpath = os.path.join(BASE_DIR, filename)
        if platform.system() == 'Windows':
            fpath = fpath.replace("\\", '/')
        # weblog.info("download: {}".format(fpath))
        # gsize = os.path.getsize(fpath)
        if not os.path.exists(fpath):
            return self.write(json.dumps({'msg': 'file not exist.', 'code': 1}))
        if not os.path.isfile(fpath):
            return self.write(json.dumps({'msg': 'not support dir.', 'code': 1}))

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + os.path.basename(urlencode_path(filename)))
        # self.set_header('Gsize', gsize)
        # self.set_header('Dmode', '0')

        if not os.path.exists(fpath):
            return self.write(json.dumps({'msg': 'error download file not exist.', 'code': 1}))
        fsize = os.path.getsize(fpath)

        # yield self.read_data(fpath, fsize)
        yield self.send_data(fpath, fsize)
        self.finish()


    @run_on_executor
    def read_data(self, fpath, flen):
        with open(fpath, 'rb') as f:

            current_read = 0
            while current_read < flen:
                if current_read + 4096 < flen:
                    f.read(4096)
                else:
                    f.read(flen - current_read)
                current_read += 4096

        # self.write(json.dumps({"msg": "success", "code": 0}))

    # @check_authenticated
    @tornado.gen.coroutine
    def post(self):
        filename = self.get_argument('filename', None)
        # brange = int(self.get_argument('brange', '0'))
        fpath = os.path.join(BASE_DIR, filename)
        # print(fpath)
        if not os.path.exists(fpath):
            return self.write(json.dumps({'msg': 'error download', 'count': -1, "error_code": 1}))
        # print(brange)
        fsize = os.path.getsize(fpath)
        yield self.send_data(fpath, fsize)
        self.finish()

    @run_on_executor
    def send_data(self, fpath, fsize=MAX_SINGLE):
        with open(fpath, 'rb') as f:
            has_read = 0
            while has_read < fsize:
                data = f.read(4096)
                if not data:
                    return
                self.write(data)
                has_read += 4096


class UploadHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    # @authenticated
    @check_authenticated
    def get(self):
        userinfo = get_user_info(self)
        curpath = self.get_argument("curpath")

        # print(userinfo)
        self.render("upload.html", userinfo=userinfo, curpath=curpath, useage=get_disk_usage(self, curpath))
        pass

    @check_authenticated
    @tornado.gen.coroutine
    def post(self):
        # filename = self.get_argument('filename', None)
        filepath = self.get_argument("curpath", None)
        urldecode_path(filepath)
        files = self.request.files['files']
        # count = 0
        for fmeta in files:
            filesize = len(fmeta['body'])
            if filesize > 523239424:
                weblog.error("file size: {} gt 500M".format(filesize))
                return self.write(json.dumps({"error_code": 1, "msg": u"文件大小超过500M"}))
            fname = fmeta['filename']
            weblog.info("{} {} {}M".format(filepath, fname, round(float(filesize * 1.0 / 1024 / 1024)), 2))
            real_file = os.path.join("/opt/data", filepath, fname)
            if os.path.exists(real_file):
                return self.write(json.dumps({"error_code": 1, "msg": u"{} 已存在".format(fname)}))
            with open(os.path.join("/opt/data", filepath, fname), 'wb') as up:  # os拼接文件保存路径，以字节码模式打开
                try:
                    up.write(fmeta['body'])  # 将文件写入到保存路径目录
                except Exception as e:
                    weblog.exception("{}".format(e))
                    up.write(fmeta['body'].decode('gbk').encode('utf-8'))

                # yield self.write(str(count) + u"、")
                # yield self.write(json.dumps({"name": fname + u"上传成功" + "\n", "count": count}))  # 将上传好的路径返回
                yield self.write(fname + u"   上传成功<br />")
                # count += 1


class AppUploadHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @check_token
    def get(self):
        userinfo = get_user_info(self)
        curpath = self.get_argument("curpath")

        # print(userinfo)
        self.render("upload.html", userinfo=userinfo, curpath=curpath, useage=get_disk_usage(self, curpath))
        pass

    @check_token
    @tornado.gen.coroutine
    def post(self):
        # filename = self.get_argument('filename', None)
        filepath = self.get_argument("curpath", None)

        files = self.request.files['files']
        # count = 0
        for fmeta in files:
            filesize = len(fmeta['body'])
            if filesize > 523239424:
                weblog.error("file size: {} gt 500M".format(filesize))
                return self.write(json.dumps({"error_code": 1, "msg": u"文件大小超过500M"}))
            fname = fmeta['filename']
            weblog.info("{} {} {}M".format(filepath, fname, round(float(filesize * 1.0 / 1024 / 1024)), 2))
            real_file = os.path.join("/opt/data", filepath, fname)
            if os.path.exists(real_file):
                weblog.error(u"{} is exist".format(real_file))
                return self.write(json.dumps({"error_code": 1, "msg": u"上传失败，{} 已存在".format(fname)}))
            with open(os.path.join("/opt/data", filepath, fname), 'wb') as up:  # os拼接文件保存路径，以字节码模式打开
                up.write(fmeta['body'])  # 将文件写入到保存路径目录

                # yield self.write(str(count) + u"、")
                # yield self.write(json.dumps({"name": fname + u"上传成功" + "\n", "count": count}))  # 将上传好的路径返回
                # yield self.write(fname + u"   上传成功<br />")
                yield self.write(json.dumps({"msg": fname + u"   上传成功<br />", "error_code": 0}))
                # count += 1