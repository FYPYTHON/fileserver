# coding=utf-8
"""
created: 10/3
"""
import time
from datetime import datetime
from database.tbl_account import TblAccount
from handlers.basehd import BaseHandler
from json import dumps as json_dumps
from tornado.log import app_log as weblog
from method.data_encode import MD5
# from handlers.common_handler import get_expires_datetime
from common.global_func import get_expires_datetime
from common.msg_def import SESSION_ID, USER_IS_NONE, USER_OR_PASSWORD_ERROR, VER_CODE_ERROR, VER_CODE_EXPER


class LogoutHandler(BaseHandler):
    def get(self):
        weblog.info("%s ,logout", self._request_summary())
        self.clear_cookie(SESSION_ID)
        self.redirect('/login')


class LoginHandler(BaseHandler):

    def get(self):

        self.render("login.html")

    def post(self):
        weblog.info("tbl_admin:%s", self.localVariable)
        try:
            userAccount = self.get_argument("userAccount", None)
            password = self.get_argument("password", None)
            inputCode = self.get_argument("inputCode", None)
        except Exception as e:
            return self.write(json_dumps({"msg": USER_IS_NONE, "error_code": 1}))
        weblog.info("{} {} {}".format(userAccount, password, inputCode))
        user = self.mysqldb().query(TblAccount.loginname, TblAccount.password, TblAccount.nickname
                                    ).filter_by(loginname=userAccount).first()
        user_update = self.mysqldb().query(TblAccount).filter_by(loginname=userAccount).first()
        if user is None:
            return self.write(json_dumps({"msg": USER_IS_NONE, "error_code": 1}))
        if user.loginname != userAccount or user.password != MD5(password):
            weblog.error("user password input:{}, ori:{}".format(user.password, MD5(password)))
            return self.write(json_dumps({"msg": USER_OR_PASSWORD_ERROR, "error_code": 1}))

        # secure_code = self.get_secure_cookie('code').decode('utf-8').upper()
        if inputCode.upper() == "APP":
            if 'Mobile' in self.request.headers['User-Agent']:
                weblog.info("mobile login : {}".format(self.request.headers['User-Agent']))
                token = MD5(str(datetime.now().timestamp()) + "APP")
                user_update.token = token
                user_update.last_logintime = datetime.now()
                self.mysqldb().commit()
                return self.write(json_dumps({"msg": "", "error_code": 0, "user": user.loginname, "token": token}))
            pass
        else:
            secure_code = self.get_secure_cookie('code')
            if secure_code:
                secure_code = secure_code.decode('utf-8').upper()
            else:
                return self.write(json_dumps({"msg": VER_CODE_EXPER, "error_code": 1}))
            if inputCode.upper() != secure_code:
                weblog.error("code you inut:{}, ori code:{}".format(inputCode.upper(),
                            self.get_secure_cookie("code").decode('utf-8').upper()))
                return self.write(json_dumps({"msg": VER_CODE_ERROR, "error_code": 1}))

        user_update.last_logintime = datetime.now()
        self.mysqldb().commit()
        # self.set_secure_cookie(SESSION_ID, user.loginname, expires=get_expires_datetime(self), expires_days=1)
        self.set_secure_cookie(SESSION_ID, user.loginname, expires=get_expires_datetime(self), expires_days=None)
        return self.write(json_dumps({"msg": "", "error_code": 0, "user": user.loginname}))


