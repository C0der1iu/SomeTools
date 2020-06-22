#encoding = utf-8
"""
@扫描模块
@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: creeper.py
@Time: 2019/2/15 14:02
"""
import re
import requests


class Creeper:
    target_url = ''
    target_list = []
    headers = {'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)'}

    def __init__(self, url):
        print('[o] 动态链接爬虫初始化中...')
        self.target_url = url

    # 查找页面的动态链接
    def find_dynamic_url(self):
        text = ''
        url_list = []
        try:
            print('[0] 正在查找{0}的动态链接'.format(self.target_url))
            req = requests.get(self.target_url, timeout=5, headers = self.headers)
            text = req.text
        except Exception:
            print('[x] 访问失败')
        # 第一种匹配全部动态链接 第二种匹配相对动态链接
        match = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$\-=$@.&\/\?])+', text)
        match2 = re.findall(r'(?<=href=").*?(?=")', text)
        if match2 != []:
            for url in match2:
                if 'http' not in url:
                    match.append(self.target_url + '/' + url)
                else:
                    match.append(url)
        for url in match:
            if '#' in url:
                url = url.split('#')[0]
            if re.findall(r'(?<=\?).*?(?==)', url) and re.findall(r'(?<=(php|asp)).*?(?==)', url) and 'gov' not in url:
                if '&' not in url:
                    url_list.append(url)
                else:
                    base_url = url.split('&')[0]
                    split_url = url.split('&')
                    url_list.append(base_url)
                    for i in range(url.count('&')):
                        url_list.append(split_url[0] + '&' + split_url[i+1])
                print('[+] 爬到 {0}'.format(url_list[-1]))
        self.target_list = list(set(url_list))
                    # print(re.split(r'(?<==).*?(?=&)', url))

