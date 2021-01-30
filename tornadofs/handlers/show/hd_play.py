# coding=utf-8
"""
created: 12/13
"""
import os
from io import BytesIO
import base64
from PIL import Image
import json

from common.msg_def import IMAGE_SUFFIX
from handlers.basehd import BaseHandler, check_authenticated, check_token
from tornado.log import app_log as weblog
from handlers.author.hd_main import get_paths, get_paths_app
import platform


def get_img_base64(realpath, suffix):
    if suffix == "jpg":
        suffix = "jpeg"
    img = Image.open(realpath)
    img_size = os.path.getsize(realpath)
    weblog.info("image wh: {} size:{}".format(img.size, img_size))
    beishu = img_size / 1024 / 1024
    sizebs = max(img.size) / 1000
    beishu = beishu if beishu > sizebs else sizebs
    if beishu > 1:
        small_size = (int(img.size[0] / beishu), int(img.size[1] / beishu))
    else:
        small_size = img.size
    img = img.resize(small_size, Image.ANTIALIAS)
    weblog.info("resize:{}  rate:{}".format(img.size, beishu))
    output_buffer = BytesIO()
    img.save(output_buffer, format=suffix)
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data).decode()
    return base64_data, beishu


class FsPlayHandler(BaseHandler):
    # @authenticated
    @check_authenticated
    def get(self, filename):
        realpath = os.path.join(self.settings.get('top_path'), filename)
        weblog.info("{} play".format(filename))
        if "\\" in realpath:
            realpath = realpath.replace("\\", '/')
        if os.path.exists(realpath):
            pass
            # print(realpath)
        else:
            return None

        suffix = realpath.split('.')[-1]
        width, height = (600, 600)
        # print(suffix)
        ftype = None
        imgs = None

        if suffix in ['mp4', "mov"]:
            # print(realpath)
            return self.render("play.html", type=ftype, uri=filename, vsrc=realpath, iwidth=width, iheight=height)
            # return self.redirect(realpath)
        else:
            pass
            ftype = 'none'
        # print(ftype)
        if platform.system() == 'Windows':
            realpath = os.path.abspath(realpath)
        weblog.info("{} {} filename:".format(realpath, ftype, filename))
        return self.render("show.html", type=ftype, uri=filename, img=imgs, iwidth=width, iheight=height)


class AppPlayHandler(BaseHandler):

    @check_token
    def get(self, filename):
        realpath = os.path.join(self.settings.get('top_path'), filename)
        weblog.info("{} play".format(filename))
        if "\\" in realpath:
            realpath = realpath.replace("\\", '/')
        if os.path.exists(realpath):
            pass
        else:
            return self.write(json.dumps({"error_code": 1, "msg": u"视屏/图片文件不存在"}))

        suffix = realpath.split('.')[-1].lower()

        if suffix.lower() in ['mp4', "mov"]:
            return self.write(json.dumps({"vsrc": realpath, "error_code": 0, "type": "video"}))
        elif suffix.lower() in IMAGE_SUFFIX:
            base64_data, beishu = get_img_base64(realpath, suffix)
            weblog.info("img base64: {}M len:{}".format(beishu, len(base64_data)))
            return self.write(json.dumps({"vsrc": realpath, "error_code": 0, "type": "image", "img": base64_data}))
        else:
            return self.write(json.dumps({"error_code": 1, "msg": u"不是视屏/图片文件"}))

    @check_token
    def post(self, filename):
        action = self.get_argument("action", "next")
        curpath = self.get_argument("curpath", None)
        index = int(self.get_argument("index", "0"))
        ftype = self.get_argument("ftype", None)
        weblog.info("action:{} curpath:{} index:{} ftype: {}".format(action, curpath, index, ftype))
        if curpath is None or ftype is None:
            return self.write(json.dumps({"error_code": 1, "msg": u"参数错误"}))

        realpath = os.path.join(self.settings.get('top_path'), curpath)
        if not os.path.exists(realpath):
            return self.write(json.dumps({"error_code": 1, "msg": u"获取文件列表失败"}))
        if action == "next":
            index = index + 1
        else:
            index = index - 1

        filelist = get_paths_app(realpath)[1]
        weblog.info("files length:{} curindex:{}".format(len(filelist), index))
        if index >= len(filelist) and action == "next":
            return self.write(json.dumps({"error_code": 1, "msg": u"最后一张"}))

        if index < 0 and action == "previous":
            return self.write(json.dumps({"error_code": 1, "msg": u"第一张"}))

        nowfile = os.path.join(curpath, filelist[index])
        realfile = os.path.join(self.settings.get('top_path'), nowfile)
        suffix = realfile.split(".")[-1].lower()
        if suffix not in IMAGE_SUFFIX:
            return self.write(json.dumps({"error_code": 1, "msg": u"不是图片文件"}))
        base64_data, beishu = get_img_base64(realfile, suffix)

        return self.write(json.dumps({"error_code": 0, "nowfile": nowfile, "msg": u"获取成功",
                                      "img": base64_data, "index": index, "vsrc": nowfile}))
