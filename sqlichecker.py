#encoding = utf-8
"""
@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: sqlichecker.py
@Time: 2019/4/1 20:29
"""
import sqli
import threading
import time
target_list = []
target_url = 'http://127.0.0.1/sqli/Less-{0}/?id=1'
starttime = time.time()
for i in range(1,66):
    target_list.append(target_url.format(str(i)))

def Test_sqli(target):
    s = sqli.Sqli(target)
    s.check_inject()

# TS = threading.Thread(target=Test_sqli, args=(target_list[int(len(target_list)/2):],))
# TS2 = threading.Thread(target=Test_sqli, args=(target_list[:int(len(target_list)/2)],))
#         #threadpool=[TL,TL2,TS,TS2]
#         #threadpool=[TL,TL2]
# threadpool = [TS,TS2]
# for thread in threadpool:
#     thread.start()
Test_sqli(target_list)

