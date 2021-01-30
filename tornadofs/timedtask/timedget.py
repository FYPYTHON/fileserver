# coding=utf-8
from common.common_base import running_time
from common.common_base import DatetimeManage
from database.db_config import db_session
from database.tbl_browsing_history import TblBrowsingHistory
from tornado.log import app_log as weblog


def clear_history(days):
    clear_date = DatetimeManage.get_days_ago(days)
    try:
        db_session.query(TblBrowsingHistory).filter(TblBrowsingHistory.browsing_date <= clear_date).delete()
        db_session.commit()
        db_session.close()
        weblog.info("db data history clear...")
    except Exception as e:
        print(e)
        weblog.exception("data history error. {}".format(e))
    pass


if __name__ == '__main__':
    clear_date = DatetimeManage.get_days_ago(1)
    print(clear_date)
    res = db_session.query(TblBrowsingHistory).filter(TblBrowsingHistory.browsing_date <= clear_date)
    for dd in res.all():
        print(dd)
