# -*-coding:UTF-8-*-
"""
Maded By @Ricky
Date:2022-03-27 19:38
"""
from ftplib import FTP
import os

class FtpDown:

    def __init__(self, ip, port, timeout, username, password):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.username = username
        self.password = password

    def ftpConnect(self):
        ftp = FTP()
        ftp.connect(self.ip, self.port, self.timeout)
        ftp.login(self.username, self.password)
        return ftp

    def downloadFile(self, ftp, remotepwd, localdir):
        ftp.cwd(remotepwd)
        list = ftp.nlst()
        for name in list:
            print(f"[+]Download: {name}")
            path = localdir + name
            fp = open(path, "wb")
            filename = f"RETR {name}"
            ftp.retrbinary(filename, fp.write)
            ftp.set_debuglevel(0)
            fp.close()

if __name__ == "__main__":
    # configuration
    VPS = "81.70.101.91"
    PORT = 9999
    TIMEOUT = 30
    USER = "anonymous"
    PASS = "anonymous"
    # WorkDir
    remotepwd = "test"
    localdir = "/tmp/"

    ftpServer = FtpDown(VPS, PORT, TIMEOUT, USER, PASS)
    ftp = ftpServer.ftpConnect()
    ftpServer.downloadFile(ftp, remotepwd, localdir)