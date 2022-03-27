# Work on VPS Server
ip = "0.0.0.0"
masquerade_address = "81.70.101.91"
port = 9999
conf = "conf/user.conf"

#上传速度  300kb/s
max_upload = 300 * 1024

#下载速度 300kb/s
max_download = 300 * 1024

#最大连接数
max_cons = 150

#最多IP数
max_per_ip = 10

#被动端口范围，注意被动端口数量要比最大IP数多，否则可能出现无法连接的情况
passive_ports = (2000, 2300)

#是否开启匿名访问 on|off
enable_anonymous = 'off'

#匿名用户目录
anonymous_path = '.'

#是否开启日志 on|off
enable_logging = 'off'

#日志文件
loging_name = 'pyftp.log'

#欢迎信息
welcome_msg = 'Welcome to Ricky ftp Demo'