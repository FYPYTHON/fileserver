# coding=utf-8
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
from settings import urls
import tornado.options
import logging.config
from tornado.log import app_log as weblog
from settings.logConfig import logConfig
import warnings

from timedtask.getcurrentjj import gene_jijin_current
from timedtask.timedget import clear_history
from timedtask.getjijindata import gene_jijin_data

warnings.filterwarnings("ignore")
from tornado.options import define, options

define("port", default=9080, help="run on the given port", type=int)
logging.config.dictConfig(logConfig)
MAX_STREAMED_SIZE = 1024 * 1024 * 1024
SSL_OPTIONS = {
    "certfile": os.path.join("/opt/data/tornadofs", "server.crt"),
    "keyfile": os.path.join("/opt/data/tornadofs", "server.key.unsecure"),
}
def check_path_exist():
    if not os.path.exists("/opt/data"):
        os.makedirs('/opt/data/public')
        os.makedirs('/opt/data/private')
    if not os.path.exists('/opt/log/fs'):
        os.makedirs('/opt/log/fs')
    if not os.path.exists("/home/trash"):
        os.makedirs('/home/trash')


class Application(tornado.web.Application):
    def __init__(self):

        settings = dict(
            template_path=(os.path.join(os.path.dirname(__file__), "templates")),
            static_path=(os.path.join(os.path.dirname(__file__), "static")),
            cookie_secret="f6d4f6de102f29b5cd37cd5eQtsdfsfdsdJ5/xJ89E=",
            session_secret="12f29b5c61c118ccd37cd5eQtsdfsfdsdJ5/xJ89E=",
            session_timeout=300,   # seconds
            token_timeout=10,   # minutes
            days_clear=7,
            upload_path=os.path.join("/opt/data", "public"),
            top_path="/opt/data",
            login_url="/login",
            debug=True,
            autoescape=None,
            xheaders=True,
            # xsrf_cookies=True,
        )

        handlers = urls.url
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    try:
        import setproctitle
        setproctitle.setproctitle("tornadofs")     # set process name in linux environment
    except:
        pass
    check_path_exist()
    # gene_jijin_data()
    # gene_jijin_current()
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app, max_buffer_size=4 * MAX_STREAMED_SIZE)
    http_server.listen(options.port)
    # http_server.bind(options.port)
    try:
        http_server.start(2)    # linux use mutli process
    except:
        print("window app start...")
        pass
    # app.listen(options.port)
    # from timedtask.timedget import printLineFileFunc
    tornado.ioloop.PeriodicCallback(lambda: clear_history(app.settings.get("days_clear")),
                                    1000 * 60 * 60 * 12).start()  # ms
    # timed task
    # tornado.ioloop.PeriodicCallback(lambda: gene_jijin_data(),
    #                                 1000 * 5).start()  # ms
    weblog.info("-- tornadofs server start .... pid:{} ".format(os.getpid()))
    tornado.ioloop.IOLoop.instance().start()



