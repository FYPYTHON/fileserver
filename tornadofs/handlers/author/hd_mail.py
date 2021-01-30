#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 14:50
# @Author  : 1823218990@qq.com
# @File    : hd_mail.py
# @Software: PyCharm

# -*- coding: utf8 -*-
import socket
from email.header import Header
from email.mime.text import MIMEText
import smtplib
from tornado.log import app_log as weblog
import json
from common.global_func import get_user_info, get_user_info_app
from handlers.basehd import BaseHandler, check_token


class EmainHandler(BaseHandler):
    @check_token
    def post(self):
        strcode = self.get_argument("code", None)

        print(strcode)
        res = self.sendEmail(self, strcode)
        return self.write(json.dumps({"error_code": int(res), "msg": ""}))
        pass


    @staticmethod
    def sendEmail(self,  msg):
        """
        邮件通知
        :param str: email content
        :return:
        """
        try:
            loginname = self.get_argument("loginname", None)
            user = get_user_info_app(self, loginname)
            if user is None:
                weblog.error(u"用户邮箱获取失败：{}".format(user))
                return False
            else:
                receiver = user.email
            if "email" in self.localVariable.keys():
                sender = self.localVariable.get("email")
                subject = '恭喜，您已订票成功'
                username = self.localVariable.get("email")
                password = self.localVariable.get("emailpwd")
                host = "smtp.126.com"
                s = "{0}".format(msg)

                msg = MIMEText(s, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
                msg['Subject'] = Header(subject, 'utf-8')
                msg['From'] = sender
                msg['To'] = receiver
                # print(sender, receiver, username, password)
                weblog.log("send:{}  to receiver:{}".format(sender, receiver))
                try:
                    smtp = smtplib.SMTP_SSL(host)
                    smtp.connect(host)
                except socket.error:
                    smtp = smtplib.SMTP()
                    smtp.connect(host)
                smtp.connect(host)
                smtp.login(username, password)
                smtp.sendmail(sender, receiver.split(","), msg.as_string())
                smtp.quit()
                weblog.info(u"邮件已通知, 请查收")
                return True
        except Exception as e:
            weblog.error(u"邮件配置有误{}".format(e))
            return False


if __name__ == '__main__':
    pass