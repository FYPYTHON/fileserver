#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 10:26
# @Author  : wangguoqiang@kedacom.com
# @File    : sjclient.py.py
# @Software: PyCharm

import socket


def start_tcp_client(ip, port):
    ###create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    failed_count = 0
    while True:
        try:
            print("start connect to server ")
            s.connect((ip, port))
            break
        except socket.error:
            failed_count += 1
            print("fail to connect to server %d times" % failed_count)
            if failed_count == 100: return

    # send and receive
    while True:
        print("connect success")

        # get the socket send buffer size and receive buffer size
        s_send_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        s_receive_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

        print("client TCP send buffer size is %d" % s_send_buffer_size)
        print("client TCP receive buffer size is %d" % s_receive_buffer_size)

        receive_count = 0
        isConnect = True
        while True:
            while not isConnect:
                try:
                    print("start connect to server ", s)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, port))
                    isConnect = True
                    break
                except socket.error as e:
                    failed_count += 1
                    print(e, "fail to connect to server %d times" % failed_count)
                    import time
                    time.sleep(3)

            try:
                print(receive_count)
                msg = '{}'.format(receive_count)

                # s.send(msg.encode('utf-8'))
                print("send len is : [%d]" % len(msg), "msg is:", msg)

                # print(s)
                msg = s.recv(1024)

                # print(msg.decode('utf-8'))
                print("recv len is : [%d] msg is: %s" % (len(msg), msg.decode('utf-8')))

                import time
                # time.sleep(0.001)
                time.sleep(3)

                receive_count += 1

                if receive_count % 5 == 0:
                    msg = 'disconnect'
                    print("total send times is : %d " % receive_count)
                    s.send(msg.encode('utf-8'))
                    isConnect = False
                    s.close()
                if receive_count == 50:
                    break
            except Exception as e:
                isConnect = False
                s.close()
                print(e)
        break

if __name__ == '__main__':
    # ip = "127.0.0.1"
    ip = "172.16.83.87"
    start_tcp_client(ip, 5062)