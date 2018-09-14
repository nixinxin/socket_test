import selectors
import socket
import logging
import sys

# 创建Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 创建终端Handler
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

# 添加到Logger中
logger.addHandler(consoleHandler)

# 创建一个selctor对象
# 在不同的平台会使用不同的IO模型,比如Linux使用epoll, windows使用select(不确定)
# 使用select调度IO
sel = selectors.DefaultSelector()


# 回调函数,用于接收新连接
def accept(sock, mask):
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


# 回调函数,用户读取client用户数据
def read(conn, mask):
    data = conn.recv(1024)  # Should be ready
    try:
        index_content = '''HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n
        
        '''
        f = open('index.html', 'r')
        index_content += f.read()
        conn.sendall(index_content.encode('utf-8'))  # Hope it won't block
        logging.debug(
            'connect:{}\r\nget info from client:\r\n'.format(str(conn)) + str(data, encoding='utf-8'))
    except Exception as e:
        logging.debug(e)
        logging.debug('closed connection!\n\n')
    sel.unregister(conn)
    conn.close()


# 一个事件循环,用于IO调度
# 当IO可读或者可写的时候, 执行事件所对应的回调函数
def loop():
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    # 创建一个非堵塞的socket
    try:
        ip, port = sys.argv[2].split(':')
        sock = socket.socket()
        sock.bind((ip, int(port)))
        sock.listen(1000)
        logging.debug("服务器运行在 {0}:{1}".format(ip, port))
        sock.setblocking(False)
        sel.register(sock, selectors.EVENT_READ, accept)
        loop()
    except Exception as e:
        print(e)
        logger.debug('请输入合法的主机和端口（例: python seocket_event.py -m 127.0.0.1:1234)')
