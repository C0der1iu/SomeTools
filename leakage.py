#encoding = utf-8
"""

@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: leakage.py
@Time: 2019/3/19 12:18
"""

import requests
import traceback



class Leakage:

    url_list = []
    db = ''
    file_name = ''
    # 主控模块，负责任务分发
    def __init__(self, filename):
        print('[o] 信息泄漏模块初始化完成！')
        self.file_name = filename
        # self.db = mysql.Mysqldb()
        # url_list = url_list
        # print(url_list)
        # for url in url_list:
        #     self.check(url)

    def get_check_url(self, url):
        rar = url.split('//')[1]
        rar2 = rar.replace('.','_')
        domain = rar.split('.')[1]
        list = []
        dic = [
            #'.git/HEAD',
            #'.svn/entries',
            #'.DS_Store',
            #'.svn/wc.db',
            'www',
            'wwwroot',
            '1',
            '0',
            '123',
            'backup',
            'backupfile',
            'backupdata',
            'backupdata',
            'data',
            'database',
            rar,
            rar2,
            domain,
        ]
        for i in dic:
            for back in ['.rar','.zip','.tar.gz','.tar','.7z','.gz']:
                yield url + '/' + i + back

    # 检测模块
    def check(self, url):
        headers = {'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)'}
        for item in self.get_check_url(url):
            try:
                print('[+] {} 正在探测...'.format(item))
                response = requests.get(item, headers=headers, timeout=5,stream=True)
                print(response.status_code)
                if response.status_code == 200:
                    cont = response.raw.read(1)
                    # print(cont)
                    capt = response.headers['Content-Type']
                    # print(capt)
                    if cont != b'' and cont != b'<' and 'application' in capt and 'json' not in capt :
                        files = open(self.file_name + '.txt', 'a')
                        files.write(item+'\n')
                        files.close()
                        print('[+] {} 探测成功，已经写入文件'.format(item))
            except Exception:
                print('[x] {} 探测失败'.format(item))
                traceback.print_exc()
