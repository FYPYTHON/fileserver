# coding=utf-8
import os
import datetime
import json
from datetime import timedelta
from urllib.parse import urlencode
import tornado.web
from tornado import gen
import tornado.options
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
# from tornado.web import authenticated
from tornado.log import app_log as weblog
from tornado.log import access_log as accesslog
from urllib.parse import unquote
from common.global_func import get_expires_datetime, get_user_info
from database.db_config import db_session
from database.tbl_admin import TblAdmin
from common.msg_def import SESSION_ID, FAIL, TOKEN_OUT
from database.tbl_account import TblAccount


# import redis


class BaseHandler(tornado.web.RequestHandler):
    localStore = {}

    def __init__(self, *argc, **argkw):
        self.remote_ip = "127.0.0.1"
        # print("init...")
        #
        # self.session = None
        # self.redis = redis.StrictRedis(host='localhost', port=6379, password='feiying')
        super(BaseHandler, self).__init__(*argc, **argkw)
        # self.session = redis_session.Session(self.application.session_manager, self)
        # print(self.request.uri, self.request.arguments)
        pass

    @gen.coroutine
    def initialize(self):
        pass

        # def __init__(self, *argc, **argkw):
        """
        定义 handler 的 session, 注意，根据 HTTP 特点.
        每次访问都会初始化一个 Session 实例哦，这对于你后面的理解很重要
        """
        # self.session = redis_session.Session(self.application.session_manager, self)
        # print("initalize...", self.session)
        self.localVariable = {}
        self.initLocalVariable()
        # yield self.browsing_history()
        # super(BaseHandler, self).__init__(*argc, **argkw)

    def prepare(self):
        self.xsrf_token
        self.browsing_history()
        remote_ip = self.request.headers.get("X-Real-Ip", "")
        self.remote_ip = remote_ip
        weblog.info("{} {} {}  remote_ip:{} user:{}, args:{}".format(os.getpid(), self.request.method,
                                                                     unquote(self.request.uri), remote_ip,
                                                                     self.current_user, self.request.arguments))

    def get_template(self, name):
        """Return the jinja template object for a given name
           jinja must not have - in template ,block end use endblock
        """
        template_dirs = []
        if self.settings.get('template_path', ''):
            if '/' in name:
                tdir, tname = name.split('/', 1)
            else:
                tdir, tname = None, name
            template_path = self.settings['template_path']
            # print(tdir, tname)
            if tdir is not None:
                template_path = os.path.join(template_path, tdir)
            template_dirs.append(template_path)

            template_path = template_path.replace('\\', '/')
            # print(template_path)
            # template_path = ['C:\\workSpace\\python\\project\\WBMSBT\\templates']
            # jenv_opt = {"autoescape": True}
            # env = Environment(loader=FileSystemLoader(template_path), extensions=['jinja2.ext.i18n'], **jenv_opt)
            env = Environment(loader=FileSystemLoader(template_path))
            try:
                # tname = 'testclick.html'
                tp = env.get_template(tname)
                # print(tp)
            except:
                raise tornado.web.HTTPError(404, "template not found : %s " % tname)
            return tp
        else:
            raise tornado.web.HTTPError(404, "template path not found")

    def render_template(self, name, **ns):
        ns.update(self.get_template_namespace())
        template = self.get_template(name)
        return template.render(**ns)

    # @authenticated
    def get(self, *args, **kwargs):
        pass

    # @authenticated
    def post(self, *args, **kwargs):
        pass

    def mysqldb(self):
        return db_session

    def on_finish(self):
        if self.current_user and self.current_user != "system":
            if isinstance(self.current_user, bytes):
                loginname = self.current_user.decode('gbk')
            else:
                loginname = self.current_user
        elif self.get_argument("loginname", None):
            loginname = self.get_argument("loginname", None)
        else:
            loginname = None
        # print(loginname, "cc")
        ten_minute_ago = datetime.datetime.now() - timedelta(minutes=self.settings.get('token_timeout'))
        user = self.mysqldb().query(TblAccount).filter(TblAccount.loginname == loginname
                                                       , ten_minute_ago < TblAccount.last_logintime).first()
        if user:
            # print(user)
            user.last_logintime = datetime.datetime.now()
            self.mysqldb().commit()
        self.mysqldb().close()

    @property
    def top_path(self):
        return self.settings.get('top_path')

    @property
    def upload_path(self):
        return self.settings.get('upload_path')

    def get_current_user(self):
        if self.request.uri.startswith(self.get_login_url()) or self.request.uri.startswith('/admin/verifyCode'):
            return "system"
        user = self.get_secure_cookie(SESSION_ID)
        if user is None:
            return None
        else:
            return user.decode('gbk')

    def initLocalVariable(self):
        variables = self.mysqldb().query(TblAdmin).all()
        for var in variables:
            if var.name not in self.localVariable.keys():
                self.localVariable[var.name] = var.value

    def browsing_history(self):
        # if self.request.method == 'GET':
        #     return 0
        if self.request.uri == "/history":
            return 0

        useragent = self.request.headers.get("User-Agent")
        if "Mobile" in useragent or "Android" in useragent:
            return 0

        login_name = self.get_current_user()
        if login_name is None:
            login_name = "未登陆用户"
        if type(login_name) == bytes:
            login_name = bytes.decode(login_name)

        if self.get_login_url() in self.request.uri:
            login_name = self.get_argument("userAccount", "system")

        remote_ip = self.request.headers.get("X-Real-Ip", "")
        if remote_ip == "":
            remote_ip = self.request.remote_ip
        try:
            self.mysqldb().execute(
                "INSERT INTO tbl_browsing_history (user_ip,user_account,request_method,"
                "uri,status,browsing_date,browsing_time,user_agent) "
                "VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');"
                % (remote_ip, login_name, self.request.uri, self.request.method,
                   self.get_status(), datetime.datetime.now().strftime('%Y%m%d'),
                   datetime.datetime.now().strftime('%H%M%S'), useragent)
            )
            self.mysqldb().commit()
        except:
            weblog.exception("BaseHandler:visit_history error")
            self.mysqldb().rollback()

    def app_history(self):
        login_name = self.get_query_argument("loginname", None)
        remote_ip = self.request.headers.get("X-Real-Ip", "")
        if remote_ip == "":
            remote_ip = self.request.remote_ip
        try:
            self.mysqldb().execute(
                "INSERT INTO tbl_browsing_history (user_ip,user_account,request_method,"
                "uri,status,browsing_date,browsing_time,user_agent) "
                "VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');"
                % (remote_ip, login_name, self.request.uri, self.request.method,
                   self.get_status(), datetime.datetime.now().strftime('%Y%m%d'),
                   datetime.datetime.now().strftime('%H%M%S'), self.request.headers.get("User-Agent"))
            )
            self.mysqldb().commit()
        except:
            weblog.exception("BaseHandler:visit_history error")
            self.mysqldb().rollback()


def check_authenticated(func):
    def inner(self, *args, **kwargs):
        user = self.get_current_user()
        # weblog.info("check_authenticated: user={} uri:{}".format(user, self.request.uri))
        if not user:
            url = self.get_login_url()
            next_url = self.request.uri
            url += "?" + urlencode(dict(next=next_url, msg=u"登录过期，请重新登录"))
            return self.redirect(unquote(url))
            # return self.write(json.dumps({"error_code": FAIL, "msg": u"登录过期，请重新登录"}))
        else:
            # if self.request.uri.startswith("/delete") and user != "Tornado" \
            #         and self.request.uri.method.lower() == "delete":
            #     return self.write(json.dumps({"error_code": FAIL, "msg": u"该操作没有权限"}))
            self.set_secure_cookie(SESSION_ID, user, expires=get_expires_datetime(self), expires_days=None)
            func(self, *args, **kwargs)

    return inner


def check_role(func):
    def inner(self, *args, **kwargs):
        user = get_user_info(self)
        if user:
            role = user.userrole
            if role > 1:
                return self.write(json.dumps({"error_code": FAIL, "msg": u"不是超级管理员，该操作没有权限"}))

        func(self, *args, **kwargs)

    return inner


def check_token(func):
    def inner(self, *args, **kwargs):
        token = self.get_argument("token", None)
        loginname = self.get_argument("loginname", None)
        check_status = False
        # print(token, loginname)
        if token and loginname:
            user = self.mysqldb().query(TblAccount).filter_by(loginname=loginname).first()
            if user:
                real_token = user.token
                if real_token == token:
                    last_login_time = user.last_logintime
                    ten_minute_ago = datetime.datetime.now() - timedelta(minutes=self.settings.get('token_timeout'))
                    # accesslog.info("last login:{} {}".format(last_login_time, ten_minute_ago))
                    if ten_minute_ago < last_login_time:
                        check_status = True
                    else:
                        weblog.info("user:{} check out last:{}".format(loginname, last_login_time))
                else:
                    last_login_time = user.last_logintime
                    ten_minute_ago = datetime.datetime.now() - timedelta(minutes=self.settings.get('token_timeout'))
                    # accesslog.info("last login:{} {}".format(last_login_time, ten_minute_ago))
                    if ten_minute_ago < last_login_time:
                        accesslog.error("user: {} login at other machine, please check.".format(loginname))
                        return self.write(json.dumps({"error_code": FAIL, "msg": u"账号在其他地方登录，"
                                                                                 u"如不是本人操作，请修改密码!",
                                                      "token": TOKEN_OUT}))
            else:
                accesslog.error("user: {} not find".format(loginname))
        else:
            accesslog.error("param loginname:{} token:{}".format(loginname, token))
        if check_status:
            # 执行post方法或get方法
            self.app_history()
            func(self, *args, **kwargs)
        else:
            weblog.info("{} login time out, please login again".format(loginname))
            return self.write(json.dumps({"error_code": FAIL, "msg": u"登录过期，请重新登录", "token": TOKEN_OUT}))

    return inner
