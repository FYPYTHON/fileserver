# coding=utf-8
"""
created: 12/13
"""
import os
from io import StringIO, BytesIO
import base64
from tornado.web import authenticated
from PIL import Image
from urllib import parse
import json
from handlers.basehd import BaseHandler, check_authenticated
from tornado.log import app_log as weblog
from common.global_func import get_user_info, resizekeepwh
import platform
TXT_FIX = ['txt', 'log', 'py']


class FsShowHandler(BaseHandler):

    @staticmethod
    def imgtobase64(imgpath, suffix, action=None, i_width=600, i_height=600):
        img = Image.open(imgpath)
        # i_width = img.size[0]
        # i_height = img.size[1]
        weblog.info("ori size :{}".format(img.size))
        if action is not None:
            if action == "zoomin":
                img = img.resize((i_width * 2, i_height * 2))
            elif action == "zoomout":
                img = img.resize((i_width // 2, i_height // 2))
            else:
                pass
        #     i_width, i_height = img.size
        # else:
        i_width, i_height = img.size

        # if i_width > 600 or i_height > 600:
        #     img = img.resize((600, 600))
        newSize = resizekeepwh(i_width, i_height)
        img = img.resize(newSize)
        # if img.size[0] < 400 or img.size[1] < 400:
        #     img = img.resize((400, 400))
        i_width, i_height = img.size
        weblog.info("reset size :{}".format(img.size))
        # imgbuff = StringIO()
        imgbuff = BytesIO()
        img.save(imgbuff, format='PNG')
        imgdata = imgbuff.getvalue()
        # print(imgdata)
        imbase64 = base64.b64encode(imgdata)
        ims = imbase64.decode()
        imgs = "data:image/{};base64,".format(suffix) + ims
        return imgs, i_width, i_height

    # @authenticated
    @check_authenticated
    def get(self, filename):
        filename = parse.unquote_plus(filename)
        realpath = os.path.join(self.settings.get('top_path'), filename)
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
        if suffix.lower() in TXT_FIX:
            ftype = "txt"
            # fdata = []
            fstr = b""
            with open(realpath, 'rb') as f:
                for line in f:
                    # fdata.append(line)
                    fstr += line
            # imgs = fdata
            imgs = fstr
            # print(fdata)
        elif suffix.lower() in ['jpg', 'png', 'gif', 'jpeg']:
            ftype = 'img'
            imgs, width, height = self.imgtobase64(realpath, suffix)
            pass
        elif suffix.lower() in ['mp4']:
            return self.render("play.html", type=ftype, uri=filename, vsrc=realpath, iwidth=width, iheight=height)
        else:
            pass
            ftype = 'none'
        # print(ftype)
        if platform.system() == 'Windows':
            realpath = os.path.abspath(realpath)
        weblog.info("{} {} filename:".format(realpath, ftype, filename))
        try:
            return self.render("show.html", type=ftype, uri=filename, img=imgs, iwidth=width, iheight=height)
        except Exception as e:
            ftype = None
            imgs = e
            return self.render("show.html", type=ftype, uri=filename, img=imgs, iwidth=width, iheight=height)

    # @authenticated
    @check_authenticated
    def post(self, filename):
        action = self.get_argument("action", None)
        iwidth = int(self.get_argument("iwidth", "600"))
        iheight = int(self.get_argument("iheight", "600"))
        realpath = os.path.join(self.settings.get('top_path'), filename)
        if "\\" in realpath:
            realpath = realpath.replace("\\", '/')
        if os.path.exists(realpath):
            pass
        else:
            return None

        suffix = realpath.split('.')[-1]
        # width, height = (600, 600)
        ftype = None
        imgs = None
        if suffix in TXT_FIX:
            ftype = "txt"
        elif suffix in ['jpg', 'png', 'gif', 'jpeg']:
            ftype = 'img'
            imgs, iwidth, iheight = self.imgtobase64(realpath, suffix, action, iwidth, iheight)
            pass
        else:
            pass
            ftype = 'none'
        # print(ftype)
        if platform.system() == 'Windows':
            realpath = os.path.abspath(realpath)
        weblog.info("{} {} filename:".format(realpath, ftype, filename))
        # return self.render("show.html", type=ftype, uri=realpath, img=imgs)
        # print(iwidth, iheight)
        return self.write(json.dumps({"img": imgs, "uri": filename, "iwidth": iwidth, "iheight": iheight}))