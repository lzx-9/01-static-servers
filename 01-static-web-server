from socket import *
import multiprocessing
import threading

#常量明明规则：必须全部是大写的
HTML_ROOT_DIR = './html'

def handle_client(client_socket):
    """处理客户端的请求"""
    request_data = client_socket.recv(1024)
    print(request_data)
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server \r\n"
    response_body  = "hello world"
    response = response_start_line + response_headers + "\r\n" + response_body
    print("response data :", response)

    client_socket.send(bytes(response, "utf8"))

    client_socket.close()

if __name__ == '__main__':
    #创建套接字(使用tcp连接)
    server_socket = socket(AF_INET, SOCK_STREAM)

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
