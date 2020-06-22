#encoding = utf-8
"""
@一个自用的轻量级前渗透信息收集检测框架
@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: main.py
@Time: 2019/2/15 13:50
"""
#import sys,sqli,xss,creeper,subdomain,collect，leakage
import sys
import leakage
import collect
import creeper
import sqli
import threading
import mysql
import re
import traceback
import requests

mys = mysql.Mysqldb('vulhub')
#leakagetest = leakage.Leakage()

# def Test_Leakage(target_url):
#     leakagetest.check(target_url)


def Test_Sqli(target_url):
    for url in target_url:
        creeper1 = creeper.Creeper(url)
        creeper1.find_dynamic_url()
        if creeper1.target_list:
            s = sqli.Sqli(creeper1.target_list)
            s.check_inject()


def collect_domain(url_list):
    for url in url_list:
        try:
            response = requests.get(url, timeout=5)
            title = title_find(response)
            if title != ' ':
                title = title[7:-8]
                content = re.findall(r'[\u4e00-\u9fa5A-Za-z0-9]', response.text)
                content = ''.join(content)
                print('内容：',str(content))
                mys.mysql_insert('search', 'title,url,content', title + '\',\'' + url + '\',\'' + content)
        except Exception:
            continue

def title_find(response):
    try:
        if response:
            print('当前页面编码：',response.apparent_encoding)
            print('当前页面更改编码：',response.encoding)
            if response.apparent_encoding and 'GB' in response.apparent_encoding:
                response.encoding = response.apparent_encoding
            else:
                response.encoding = 'utf-8'
            res = response.text
            return re.findall(r'<title>[\s\S]*?</title>', res)[0]
        else:
            return ' '
    except Exception:
        print('提取title出错！')
        traceback.print_exc()
        return ' '


if __name__ == "__main__":
    max = 100
    test = collect.Collect('http://www.hao123.cn', max)
    target_url = 'blank'
    while (1):
        target_url = test.collect_url()
        # TL = threading.Thread(target=Test_Leakage, args=(target_url[int(max/2):],))
        # TL2 = threading.Thread(target=Test_Leakage, args=(target_url[:int(max/2)],))
        # TS = threading.Thread(target=Test_Sqli, args=(target_url[int(max/2):],))
        # TS2 = threading.Thread(target=Test_Sqli, args=(target_url[:int(max/2)],))
        CU1 = threading.Thread(target=collect_domain, args=(target_url[int(max/2):],))
        CU2 = threading.Thread(target=collect_domain, args=(target_url[:int(max/2)],))
        # CU3 = threading.Thread(target=Test_Sqli, args=(target_url[int(max/2):],))
        # CU4 = threading.Thread(target=Test_Sqli, args=(target_url[:int(max/2)],))
        #threadpool=[TL,TL2,TS,TS2]
        threadpool=[CU1,CU2]
        #threadpool = [TS,TS2]
        for thread in threadpool:
            thread.start()

    # f=open('edu.txt', 'r', encoding='utf-8')
    # line = f.readline()
    # i = 0
    # target_url=[]
    # while line != '':
    #     line = 'http://'+f.readline()[:-1]
    #     line2 = 'https://'+f.readline()[:-1]
    #     if i<20:
    #         target_url.append(line)
    #         target_url.append(line2)
    #         print(target_url)
    #         i+=1
    #     else:
    #         leakagetest = leakage.Leakage(target_url)
    #         for url in target_url:
    #             creeper1 = creeper.Creeper(url)
    #             creeper1.find_dynamic_url()
    #             if creeper1.target_list:
    #                 s = sqli.Sqli(creeper1.target_list)
    #                 s.check_inject()
    #         i=0
    #         target_url=[]


