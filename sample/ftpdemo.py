# -*-coding:UTF-8-*-
"""
Maded By @Ricky
Date:2022-03-27 19:18
Authorization Introduction
-----------------------------
| 读权限 | 作用              |
| ------ | -----------------|
| e      | 改变文件目录      |
| l      | 列出文件          |
| r      | 从服务器接收文件   |
-----------------------------
----------------------------------------------
| 写权限 | 作用                               |
| ------ | ----------------------------------|
| a      | 文件上传                           |
| d      | 删除文件                           |
| f      | 文件重命名                         |
| m      | 创建文件                           |
| w      | 写权限                             |
| M      | 文件传输模式（通过FTP设置文件权限    |
----------------------------------------------
"""
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from conf import settings
import logging

class FtpDemo:

    def __init__(self, ip, vps, port, conf, anonymous, log):
        self.ip = ip
        self.vps = vps
        self.port = port
        self.conf = conf
        self.anonymous = anonymous
        self.log = log

    def FtpInit(self):
        # Init Visual User
        authorize = DummyAuthorizer()

        userList = self.getUser(self.conf)
        for user in userList:
            USER, PASS, PERMIT, FOLDER = user
            # Add user authorization (username, password, work folder, authorization)
            authorize.add_user(USER, PASS, FOLDER, perm=PERMIT)

        if self.anonymous == 'on' and settings.anonymous_path != "":
            # Add Anonymous User, only with work folder (Default in current folder)
            authorize.add_anonymous(settings.anonymous_path)

        # Upload And Download Speed
        dtp_handler = ThrottledDTPHandler
        dtp_handler.read_limit = settings.max_download
        dtp_handler.write_limit = settings.max_upload

        # Init Handler
        handler = FTPHandler
        handler.authorizer = authorize

        # Log
        if self.log == 'on' and settings.loging_name != "":
            logging.basicConfig(filename=settings.loging_name, level=logging.INFO)

        # Welcome Message
        handler.banner = settings.welcome_msg

        # Masquerade address
        handler.masquerade_address = self.vps

        # Add Passive Port
        handler.passive_ports = range(settings.passive_ports[0], settings.passive_ports[1])

        # Work on VPS
        server = FTPServer((self.ip, self.port), handler)

        # Max Connection
        server.max_cons = settings.max_cons
        server.max_cons_per_ip = settings.max_per_ip

        # Server Start
        print(f'FTPServer working on [0.0.0.0] (family 0, port {self.port})')
        server.serve_forever()

    def getUser(self, conf):
        userList = []
        with open(conf) as fp:
            for line in fp:
                # print(len(line.split()))
                if not line.startswith("#") and line:
                    if len(line.split()) == 4:
                        userList.append(line.split())
                    else:
                        raise Exception(f"Wrong Configuration: {conf}")
        return userList

if __name__ == "__main__":
    FtpDemo(settings.ip, settings.masquerade_address, settings.port, settings.conf, settings.enable_anonymous, settings.enable_logging).FtpInit()

