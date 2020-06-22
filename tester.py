#encoding = utf-8
"""

@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: tester.py
@Time: 2019/5/12 22:13
"""

import mysql,PortScanner,threading,leakage
scanner = PortScanner.PortScan()
mys = mysql.Mysqldb('vulhub')
url_list = []


def scan_port_from_url(url):
    scanner.set_remote_url(url)


def select_url_from_db(target):
    res = mys.mysql_select('urls', 'url', 'url like \'%{}%\''.format(target),'')
    for url in res.fetchall():
        url_list.append(str(url)[2:-3])

def insert_result_to_db(url, port):
    mys.mysql_insert('url_portscan','url,open_port',url + '\',\'' + str(port))

# select_url_from_db('.vivo.com')
# select_url_from_db('.sina.com')
# select_url_from_db('.qq.com')

# for url in url_list:
#     scanner.set_remote_server(url)
#     open_port = scanner.start_scan(50)
#     print(open_port)
#     scanner.reset_open_port()

leak = leakage.Leakage('sina')
select_url_from_db('.sina.com')

for url in url_list:
    leak.check(url)
#
# # url = 'https://id.vivo.com.cn'
# #
# # scanner.set_remote_server(url)
# # open_port = scanner.start_scan(50)
# # print(open_port)