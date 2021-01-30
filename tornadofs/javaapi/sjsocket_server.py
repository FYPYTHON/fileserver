#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/15 19:36
# @Author  : 1823218990@qq.com
# @File    : sjsocket_server.py
# @Software: PyCharm
# server use to handle client message

import socket
import sys
import time
import threading
HEARTBEAT_TIME = 10
SEND_BUF_SIZE = 1024
RECV_BUF_SIZE = 1024

all_client = dict()
def heartbeat():
    # print(threading.enumerate().__str__())
    for t_thread in threading.enumerate():
        # print(t_thread)
        # print(t_thread.__dict__)

        if t_thread.__str__().startswith("<Thread"):
            print(t_thread.__str__())

    hb = threading.Timer(HEARTBEAT_TIME, heartbeat)
    hb.start()
    pass

def start_tcp_server(ip, port):
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)

    # bind port
    print("starting listen on ip %s, port %s" % server_address)
    sock.bind(server_address)

    # set a new buffer size
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)

    # start listening, allow only [n] connection
    try:
        sock.listen(4)   # n=4
    except socket.error as e:
        print("fail to listen on port %s" % e)
        sys.exit(1)

    receive_count = 1

    # client, addr = sock.accept()
    # print(addr)
    while True:
        while True:
            print("waiting for connection")
            client, addr = sock.accept()
            print("having a connection")
            # print(client, addr)
            all_client[addr[0]] = client
            t1 = threading.Thread(target=handle_message, args=(client, addr), name=str(addr))
            t1.start()
            # t1.join()
            # handle_message(client, addr)
            # print(threading.enumerate().__str__())
            print(all_client)

            if receive_count > 2:
                break
        break

    print("finish test, close connect")
    client.close()
    sock.close()
    print(" close client connect ")


def handle_message(client, addr):

    receive_count = 1
    while True:
        try:
            msg = client.recv(1024)
            msg_de = msg.decode('utf-8')
            if msg_de == "#all":
                for key, cli in all_client.items():
                    cli.send("must to change status".encode('utf-8'))
            # print("recv len is : [%d] msg: %s" % (len(msg_de), msg_de))

            if msg_de == '#stop_server':
                print("receiver stop server signal, then break...")
                break
            # print(client)
            msg = ("hello, %s, i got your msg %d times, now i will send back to you.%s" % (addr, receive_count, msg_de))

            client.send(msg.encode('utf-8'))
            receive_count += 1
        except Exception as e:
            print(e, client, "sleep 3s")
            print(client, type(client))
            client.close()
            time.sleep(3)
            break

if __name__ == '__main__':
    hb = threading.Timer(HEARTBEAT_TIME, heartbeat)
    hb.start()
    # ip = "127.0.0.1"
    ip = "172.16.83.87"
    # ip = "192.168.0.87"

    start_tcp_server(ip, 5062)
