"""

@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: multithread.py
@Time: 2019/4/16 13:47
"""

import threading
import time
import collect
timer=0
balance = 0
caipin=''
name =''
test =collect.Collect('http://www.2345.com',10)
def huoguo(caipin):
  #  time.sleep(2)
    print('老子吃'+str(caipin))
    time.sleep(2)


def movie(name):
    print('老子看电视,今晚播放'+str(name))
    time.sleep(2)

def collect(name):
    global timer
    time.sleep(5)
    return name+str(timer)
while 1:
    target_url = test.collect_url()
    t1 = threading.Thread(target=huoguo, args=(target_url[5:],))
    t2 = threading.Thread(target=huoguo, args=(target_url[:5],))
    threadpool = []
    threadpool.append(t1)
    threadpool.append(t2)
    for t in threadpool:
        t.start()
    print('开始了')

    print('看完了')
