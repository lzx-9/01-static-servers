from socket import *
import multiprocessing
import threading
import re
import os
import sys

#常量明明规则：必须全部是大写的
HTML_ROOT_DIR = sys.path[0] + '\html'

def handle_client(client_socket):
    """处理客户端的请求"""
    print(HTML_ROOT_DIR + '*' *20)
    request_data = client_socket.recv(1024)

    print("request_data: ",request_data)
    request_lines = request_data.decode("utf-8").splitlines()
    for line in request_lines:
        print(line)

    #报文解析，提取变量
    request_start_line = request_lines[0]
    file_name = re.match(r"\w+ (/[^ ]* )", str(request_start_line)).group(1)
    print('*' * 20)
    print(file_name)

    try:
        #打开文件，提取内容
        print(HTML_ROOT_DIR + file_name)
        file = open(HTML_ROOT_DIR + file_name, "r")
        file_data = file.read()
        file.close()
    except IOError:
        request_start_line = "HTTP/1.1 200 OK\r\n"
        request_header = "Server: my server\r\n"
        request_body = "the file is not found"
    else:
        request_start_line = "HTTP/1.1 200 OK\r\n"
        request_header = "Server: my server\r\n"
        request_body = file_data
    finally:
        response = request_start_line + str(request_header) + "\r\n" + request_body
        print(response)
        client_socket.send(bytes(response, "utf-8"))

    client_socket.close()

if __name__ == '__main__':
    #创建套接字(使用tcp连接)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET , SO_REUSEADDR, 1)

    #创建地址
    address =('',int('8000'))

    #创建绑定
    server_socket.bind(address)

    #创建监听
    server_socket.listen(120)

    #建立连接
    while True:
        client_socket, client_address = server_socket.accept()
        handle_client_progress = multiprocessing.Process(args=(client_socket,), target=handle_client)
        handle_client_progress.start()
        client_socket.close()

