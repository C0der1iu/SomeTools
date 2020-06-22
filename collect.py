#encoding = utf-8
"""

@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: collect.py
@Time: 2019/2/15 14:04
"""
import requests
import re
import traceback
#import mysql


class Collect:

    size = 0
    flag = [0, 1, 1]
    dict = {}
    db = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    big_list = []
    def __init__(self, site, size):
        print('[o] 初始化收集脚本')
        #self.db = mysql.Mysqldb()
        self.size = size
        self.dict = {'list1': [site]}

    def title_find(self, response):
        try:
            if response != '':
                print('当前页面编码：',response.apparent_encoding)
                print('当前页面更改编码：',response.encoding)
                if response.apparent_encoding and 'GB' in response.apparent_encoding:
                    response.encoding = response.apparent_encoding
                else:
                    response.encoding = 'UTF-8'
                res = response.text
                return re.findall(r'<title>[\s\S]*?</title>', res)
            else:
                return 'Not Found '
        except Exception:
            print('提取title出错！')
            traceback.print_exc()

    def collect_url(self):
        # len(self.dict['list'+str(self.flag[1])]) <= self.size
        while 1:
            for i in self.dict['list'+str(self.flag[2])][self.flag[0]:]:
                #print('[i] 当前页面：'+ i)
               # print('[i] 当前任务进度： 在第' + str(self.flag[2]) + '个列表的第'+ str(self.flag[0])+'个位置，待插列表编号：' + str(self.flag[1]) +'总共有' + str(len(self.dict)) + '个列表')
                try:
                    req = requests.get(i, timeout=5)
                    print('title:')
                    print(self.title_find(req))
                    temp_list = self.find_url_widly(req.text)
                    for url in temp_list:
                        if 'gov' not in url and url not in self.big_list:
                            self.dict['list' + str(self.flag[1])].append(url)
                            self.big_list.append(url)
                            if len(self.dict['list'+str(self.flag[1])]) >= self.size:
                                self.flag[0] = self.dict['list'+str(self.flag[2])].index(i) + 1
                                if self.flag[0] == self.size :
                                    self.flag[0] = 0
                                    self.flag[2] += 1
                                self.flag[1] += 1
                                self.dict['list' + str(self.flag[1])] = []
                                return self.dict['list'+str(self.flag[1]-1)]
                    if self.flag[0] == self.size - 1:
                        self.flag[0] = 0
                        self.flag[2] += 1
                    else:
                        self.flag[0] += 1
                except Exception:
                    #traceback.print_exc()
                    print('[x] 访问失败')
                    if self.flag[0] == self.size - 1:
                        self.flag[0] = 0
                        self.flag[2] += 1
                    else:
                        self.flag[0] += 1
                    break
                    # 如果网站可以访问就入库
                    # self.db.mysql_insert(i, 'vulhub')
                # print('[+] 模拟入库:  ' + i)
                # self.url_list.remove(i)
                # print('[-] 探测完毕，目标已去除')
                # print('[o] 还剩' + str(len(self.url_list)) + '个任务')
                # print('++++++++++++++++++++++++++++++++++++++++')
            # else:
            #     print('[+] 本轮爬取任务：' + str(len(self.dict['list'+str(self.flag[1])])) + ' 个')
            #     for i in self.dict['list'+str(self.flag[1])]:
            #         print('[+] ' + i + ' 为下一个目标')
            #         try:
            #             req = requests.get(i, timeout=5)
            #             temp_list = self.find_url_widly(req.text)
            #             for url in temp_list:
            #                 if 'gov' not in url and url not in self.dict['list'+str(self.flag[1])]:
            #                     self.dict['list' + str(self.flag[1])].append(url)
            #                     if len(self.dict['list'+str(self.flag[1])]) >= self.size:
            #                         self.flag[0] = self.dict['list'+str(self.flag[1])].index(i)
            #                         if self.flag[0] != self.size - 1:
            #                             self.flag[2] = self.flag[1]
            #                         else:
            #                             self.flag[0] = 0
            #                             self.flag[2] = self.flag[1] + 1
            #                         self.flag[1] += 1
            #                         self.dict['list' + str(self.flag[1])] = []
            #                         return self.dict['list'+str(self.flag[1])]
            #         except Exception:
            #             print('[x] 访问失败')
            #             # 如果网站可以访问就入库
            #             # self.db.mysql_insert(i, 'vulhub')
            #             print('[+] 模拟入库:  ' + i)
            #             self.url_list.remove(i)
            #             print('[-] 探测完毕，目标已去除')
            #             print('[o] 还剩' + str(len(self.url_list)) + '个任务')
            #             print('++++++++++++++++++++++++++++++++++++++++')

    def find_url_widly(self, text):
        urls = re.findall(r'https?://\w+\.\w+\.?\w+\.?\w+\.?\w+', text)
        urls = list(set(urls))
        tms = len(urls)
        print('[+] 此页面找到' + str(tms) + '个URL')
        print('---------------------------------')
        return urls

    # def find_url_tinly(self, text):
    #     a = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$\-=$@.&\/\?])+', text)
    #     tms = len(a)
    #     a = list(set(a))
    #     self.url_list += a
    #     self.url_list = list(set(self.url_list))
    #     print('[+] 此页面找到' + str(tms) + '个URL')
    #     print('---------------------------------')


