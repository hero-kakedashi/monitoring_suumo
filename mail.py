# coding= utf-8
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import ssl

class Mail:
    """
    メールアドレスについて (クラス変数)
    """
    FROM_ADDRESS = 'yyyy@gmail.com'
    MY_PASSWORD = 'yyyy'
    TO_ADDRESS = 'xxxx@gmail.com'
    BCC = ''
    SUBJECT = 'GmailのSMTPサーバ経由'
    BODY = 'pythonでメール送信'


    """
    メールを送信する関数

    Parameters
    ----------
    to_addr : String
       宛先
    msg     : String
       本文
    """
    def send(self, to_addrs, msg, subject):
        content = MIMEMultipart('alternative')
        content["Subject"] = subject
        part1 = MIMEText(msg, 'plain')
        content.attach(part1)

        smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
        smtpobj.login(Mail.FROM_ADDRESS, Mail.MY_PASSWORD)
        smtpobj.sendmail(Mail.FROM_ADDRESS, to_addrs, content.as_string())
        smtpobj.close()

