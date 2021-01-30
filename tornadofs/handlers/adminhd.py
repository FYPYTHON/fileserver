# coding=utf-8
from database.tbl_account import TblAccount
from database.tbl_admin import TblAdmin
from database.tbl_code import TblCode
from handlers.basehd import BaseHandler, check_token, check_authenticated
from json import dumps as json_dumps
from common.global_func import get_expires_datetime
from method.generate_verify_image import generate_verify_image
from method.my_decode import self_decode, self_encode
import base64
import random
from tornado.log import app_log as weblog
import tornado.web

class verifyCode(BaseHandler):
    def get(self):
        pass

    def post(self):
        fg_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        try:
            mstream, strs = generate_verify_image(save_img=False, fg_color=fg_color, font_type="method/Arial.ttf")
            # self.write(simplejson.dumps({'code': 0, 'img': stream.getvalue().encode('base64')}))
            # self.set_cookie("code", strs)
            self.set_secure_cookie("code", strs, expires=get_expires_datetime(self))
            # weblog.info("%s , imgage code:%s", self.request.uri + " " + self.remote_ip, strs)
            # img = mstream.getvalue().encode('base64')
            img = base64.b64encode(mstream.getvalue()).decode()
            return self.write(json_dumps({'code': strs, 'img': img}))
        except:
            weblog.exception("verify image code error")
            return


class XSRFTokenHandler(tornado.web.RequestHandler):
    """专门用来设置_xsrf Cookie的接口"""
    def get(self):
        self.xsrf_token
        self.write("Ok")


class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write(json_dumps({"status": 0}))


class DecodeSelfHandler(BaseHandler):
    # @check_authenticated
    def get(self):
        cursuer = self.current_user if self.current_user is not None else ""
        all_code = self.mysqldb().query(TblCode).filter(TblCode.user == cursuer).all()
        code_list = []
        for codeinfo in all_code:
            code_list.append(codeinfo)
        return self.render("decode.html", codelist=code_list)

    # @check_authenticated
    def post(self):
        destr = self.get_argument("destr", "")
        bstr = destr.encode('utf-8')
        # print(bstr)
        try:
            result = self_decode(bstr)
        except Exception as e:
            weblog.error("{}".format(e))
            result = u"解密失败"
        return self.write(json_dumps({"decode": result}))





class AppVersionHandler(BaseHandler):
    """
    1.0.1
    文件上传
    1.0.2
    图片左右滑动切换
    增加个人信息
    1.0.3
    增加文件上传图片缩略图

    1.1
    增加导航界面
    增加古诗词界面
    """
    @check_token
    def get(self):
        version_info = self.mysqldb().query(TblAdmin.name, TblAdmin.value).filter(TblAdmin.name == "appversion").first()
        if version_info is None:
            return self.write(json_dumps({"error_code": 1, "msg": u"暂无版本信息", "version": "unknown"}))
        else:
            return self.write(json_dumps({"error_code": 0, "version": version_info.value, "msg": self.__doc__}))

    @check_token
    def put(self):
        version = self.get_argument("version", None)
        if version is None:
            return self.write(json_dumps({"error_code": 1, "msg": u"参数错误"}))

        version_info = self.mysqldb().query(TblAdmin).filter(TblAdmin.name == "appversion").first()
        if version:
            version_info.value = version
            self.mysqldb().commit()
            return self.write(json_dumps({"error_code": 0, "msg": u"修改成功"}))
        else:
            return self.write(json_dumps({"error_code": 1, "msg": u"暂无版本信息"}))


class UserinfoHandler(BaseHandler):
    @check_token
    def get(self):
        loginname = self.get_argument("loginname", None)
        user = self.mysqldb().query(TblAccount.loginname, TblAccount.nickname, TblAccount.email
                                    , TblAccount.last_logintime).filter(TblAccount.loginname == loginname).first()

        msg = dict()
        version_info = self.mysqldb().query(TblAdmin.value, TblAdmin.name).filter(TblAdmin.name == "appversion").first()
        if version_info is None:
            msg['version'] = "unknown"
        else:
            msg['version'] = version_info.value
        if user is None:
            msg['error_code'] = 1
            msg['msg'] = u"获取个人信息失败"
            msg['nickname'] = ""
            msg['email'] = ""
            # msg['last_logintime'] = ""
            return self.write(json_dumps(msg))
        else:
            msg['error_code'] = 0
            msg['msg'] = u"获取个人信息成功"
            msg['nickname'] = user.nickname
            msg['email'] = user.email
            if user.email == "":
                msg['email'] = u"邮箱未设置"
            # msg['last_logintime'] = ""
            return self.write(json_dumps(msg))