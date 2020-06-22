# encoding = utf-8
"""

@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: test.py
@Time: 2019/3/20 17:05
"""
import re
import requests
import sqli
import creeper
import traceback

# 功能： 找到指定url内的所有详细链接，并且从这些链接中采集到域名并返回列表


class Findpage:
    url_list = []
    target_list = []
    url = ''
    domain = ''
    headers = {'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)'}

    def __init__(self, url):
        res = ''
        self.url = url
        self.domain = url.split('.')[1]
        self.url_list = [url]
        try:
            res = requests.get(url, timeout=5, headers=self.headers).text
        except Exception:
            print('[x] URL访问失败，请检查')
        # 寻找当前页面的绝对地址和相对地址
        absolute_url = self.abusolute_url_find(res)
        relative_url = self.relative_url_find(res)
        absolute_url += relative_url
        self.url_list += list(set(absolute_url))
        self.url_list = self.make_url(self.url,self.url_list)

    def abusolute_url_find(self, res):
        return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$\-=$@.&\/\?])+\/.(?:[a-zA-Z]|[0-9]|[$\-=$@.&\/\?])+', res)

    def relative_url_find(self, res):
        return re.findall(r'(?<=href=").*?(?=")', res)

    def clear_url_find(self, res):
        return re.findall(r'https?://\w+\.\w+\.?\w+\.?\w+\.?\w+', res)

    # 这里的response不同于以往函数，为了编码，需要传入响应对象
    def title_find(self, response):
        try:
            if response != '':
                response.encoding = response.apparent_encoding
                res = response.text
                return re.findall(r'<title>[\s\S]*?</title>', res)
            else:
                return 'Not Found '
        except Exception:
            print('提取title出错！')
            traceback.print_exc()


    def make_url(self, url, url_list):
        # 将url列表中的相对地址加上前缀
        for i in url_list:
            if 'http' not in i:
                url_list[url_list.index(i)] = url + i.strip()
        return url_list

    def get_the_url_from_pages(self):
        # 从整理好的url列表中获得域名信息
        temp_list = []
        for target in self.url_list:
            print('[o] 当前扫描目标：' + target)
            try:
                res = requests.get(target, timeout=5)
            except Exception:
                print('访问失败')
            self.target_list += self.clear_url_find(res.text)
            self.target_list = list(set(self.target_list))
            # print(self.target_list)
            absolute_url = self.abusolute_url_find(res.text)
            relative_url = self.relative_url_find(res.text)
            print(self.title_find(res))
            absolute_url += relative_url
            temp_list += list(set(absolute_url))
            temp_list = self.make_url(self.url, temp_list)
            for i in temp_list:
                if len(self.url_list)<5000 and self.domain in i and i not in self.url_list:
                    print('[+] 加入一个新的链接！' + i + '当前页面数量' + str(len(self.url_list)) + '目前处理第'+str(self.url_list.index(target)) + '个页面')
                    self.url_list.append(i)


test = Findpage('https://www.sy118.com/')
test.get_the_url_from_pages()
nums = len(test.target_list)
for url in test.target_list:
    print('[+] 当前执行第' + str(test.target_list.index(url)) + '个url 任务,总共' + str(nums) + '个')
    creeper1 = creeper.Creeper(url)
    creeper1.find_dynamic_url()
    sqli1 = sqli.Sqli(creeper1.target_list)
    sqli1.check_inject()

# test.target_list