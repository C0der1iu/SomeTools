#encoding = utf-8
"""

@Author: c0d3r1iu
@Email: admin@recorday.cn
@File: PortScanner.py
@Time: 2019/5/14 15:39
"""

import socket
import threading
import math
import time


class PortScan:
    remote_server = ''
    open_port = []

    def __init__(self, remote_addr=''):
        if '://' in remote_addr:
            remote_addr = remote_addr.split('://')[1]
        self.remote_server = socket.gethostbyname(remote_addr)

    def set_remote_server(self, remote_addr):
        if '://' in remote_addr:
            remote_addr = remote_addr.split('://')[1]
        #self.remote_server = socket.gethostbyname(remote_addr)
        self.remote_server = remote_addr

    def reset_open_port(self):
        self.open_port = []

    def scan(self, start_port, end_port):
        socket.setdefaulttimeout(0.5)

        for port in range(start_port,end_port):
            try:
                sock = socket.socket(2,1)
                res = sock.connect_ex((self.remote_server,port))
                if res == 0:
                    print('Port {} : Open'.format(port))
                    self.open_port.append(port)
                    # else:
                    #     print('Port {} : Close'.format(port))
                    sock.close()
            except Exception:
                print('Can not scan the {} port'.format(port))
                continue

    def start_scan(self,thread_number):
        print('Start to scan : ', self.remote_server)
        starttime = time.time()
        threadpool = []
        port_list = []
        num = 0
        average = math.floor(10000 / thread_number)
        for rank in range(thread_number + 1):
            port_list.append(num)
            num += average
        port_list[len(port_list)-1] = 10000
        print(port_list)
        for i in range(thread_number):
            threadpool.append(threading.Thread(target=self.scan, args=(port_list[i] , port_list[i+1])))
        for thread in threadpool:
            thread.start()
        thread.join()
        print('Finish')
        print(self.open_port)
        print('Spend {} time'.format(str(time.time()-starttime)))
        return self.open_port
    # def multiThread(Startport, Endport, number):
    #     portsum = Endport - Startport
    #     port_dict = {}
    #     dict = {}
    #     for i in range(number):
    #         dict[i]=threading.Thread(target=scan, args=(target_url[:],))