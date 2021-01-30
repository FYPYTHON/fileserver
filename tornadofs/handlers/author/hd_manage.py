# coding=utf-8
"""
created: 02/17
"""
from tornado.web import authenticated
import time
from datetime import datetime
from database.tbl_account import TblAccount
from database.tbl_code import TblCode
from handlers.author.hd_main import get_disk_usage
from handlers.basehd import BaseHandler, check_authenticated, check_token, check_role
from json import dumps as json_dumps
from tornado.log import access_log as weblog
from method.data_encode import MD5
# from handlers.common_handler import get_expires_datetime
from common.global_func import get_expires_datetime, get_user_all, get_user_info, get_user_by_id
from common.msg_def import SESSION_ID, USER_IS_NONE, USER_OR_PASSWORD_ERROR, VER_CODE_ERROR
from method.my_decode import self_encode, self_decode


class ManageHandler(BaseHandler):
    @check_authenticated
    def get(self):
        curpath = self.get_argument('curpath', None)
        if curpath is None:
            curpath = 'public'
        # self.clear_cookie(SESSION_ID)
        # self.redirect('/login')
        userlist = get_user_all(self)
        userinfo = get_user_info(self)
        self.render("manage.html", users=userlist, userinfo=userinfo, curpath=curpath,
                    useage=get_disk_usage(self, curpath))

    @check_authenticated
    @check_role
    def post(self):
        loginname = self.get_argument("loginname", None)
        nickname = self.get_argument('nickname', None)
        password = self.get_argument('password', None)
        email = self.get_argument("email", None)
        userrole = self.get_argument("userrole", "2")

        if loginname == "": loginname = None
        if nickname == "": nickname = None
        if password == "": password = None
        if email == "": email = None

        user = self.mysqldb().query(TblAccount).filter(TblAccount.loginname == loginname).first()
        if user is None:
            adduser = True
        else:
            adduser = False
        if loginname is not None and nickname is not None and password is not None and email is not None:

            password = MD5(password)
            if adduser:
                user = TblAccount()
            user.password = password
            user.loginname = loginname
            user.nickname = nickname
            user.email = email
            user.userrole = userrole
            user.userstate = 0
            if adduser:
                self.mysqldb().add(user)
            try:
                self.mysqldb().commit()
                return self.write(json_dumps({"error_code": 0, "msg": u"添加成功"}))
            except Exception as e:
                self.mysqldb().rollbakc()
                weblog.error("{}".format(e))
                return self.write(json_dumps({"error_code": 1, "msg": u"添加失败"}))
        else:
            return self.write(json_dumps({"error_code": 1, "msg": u"信息不完整"}))

    @authenticated
    def delete(self, uid):
        weblog.info("uid={}".format(uid))
        try:
            self.mysqldb().query(TblAccount).filter(TblAccount.id == uid).delete()
            self.mysqldb().commit()
            return self.write(json_dumps({"error_code": 0, "msg": u"删除成功"}))
        except Exception as e:
            weblog.error("{}".format(e))
            return self.write(json_dumps({"error_code": 1, "msg": u"删除失败。{}".format(e)}))



class UserInfoHandler(BaseHandler):
    # @check_authenticated
    def get(self, id):
        user = get_user_by_id(self, id)
        if user is None:
            return self.write(json_dumps({"error_code": 1, "msg": u"获取信息失败，请刷新页面"}))
        else:
            return self.write(json_dumps({"error_code": 0, "user": user}))



class RestartHandler(BaseHandler):
    @check_token
    def post(self):
        cur_user = self.get_argument("loginname", None)
        self.restart(cur_user)

    @check_authenticated
    def get(self):
        if self.current_user:
            cur_user = self.current_user.decode('gbk')
        else:
            cur_user = None

        self.restart(cur_user)

    def restart(self, cur_user):
        user = self.mysqldb().query(TblAccount).filter(TblAccount.loginname == cur_user).first()
        TO_RESTART = False
        if user:
            if user.userrole == 0:
                TO_RESTART = True
        if TO_RESTART:
            import os
            res = os.system("bash /opt/midware/FSTornado/shell/restart.sh")
            if res == 0:
                return self.write(json_dumps({"error_code": 0, "msg": u"服务已重启"}))
            else:
                return self.write(json_dumps({"error_code": 1, "msg": u"服务重启失败"}))
        else:
            return self.write(json_dumps({"error_code": 1, "msg": u"没有操作权限"}))


class AppCodeHandler(BaseHandler):
    @check_token
    def get(self):
        pass
        loginname = self.get_argument("loginname")
        all_code = self.mysqldb().query(TblCode).filter(TblCode.key == loginname).all()
        code_list = []
        for codeinfo in all_code:
            code_list.append(codeinfo)
        return self.write(json_dumps({"codelist": code_list, "error_code": 0}))

    @check_token
    def put(self):
        enstr = self.get_argument("enstr", "")
        bstr = enstr.encode('utf-8')

        # print(bstr)
        weblog.info("enstr:{}".format(bstr))
        error_code = 0
        if len(bstr) > 20:
            error_code = 1
            return self.write(json_dumps({"decode": u"字符长度需小于20", "error_code": error_code}))
        try:
            result = self_encode(bstr)
            if isinstance(result, bytes):
                result = result.decode()
        except Exception as e:
            weblog.error("{}".format(e))
            result = u"加密失败"
            error_code = 1
        return self.write(json_dumps({"decode": result, "error_code": error_code}))

    @check_token
    def post(self):
        destr = self.get_argument("destr", "")
        bstr = destr.encode('utf-8')
        # print(bstr)
        error_code = 0
        weblog.info("destr:{}".format(bstr))
        try:
            result = self_decode(bstr)
        except Exception as e:
            weblog.error("{}".format(e))
            result = u"解密失败"
            error_code = 1
        return self.write(json_dumps({"decode": result, "error_code": error_code}))