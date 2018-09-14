"""
IO多路复用socket实例代码
"""
import socket
import select

sk1 = socket.socket()
sk1.bind(("127.0.0.1", 8001))
sk1.listen(5)
inputs = [sk1, ]
info_sender = []
message = {}

while True:
    # select自动监听文件描述符，发生变化则放入r_list列表中
    r_list, w_list, e_list = select.select(inputs, info_sender, [], 1)
    # print("正在监听的对象数量：%d" % len(inputs))
    for sk in r_list:
        # sk 表示每个连接对象
        if sk == sk1:
            # 有新用户建立连接
            conn, address = sk.accept()
            conn.sendall(bytes("欢迎进入服务端", encoding="utf-8"))
            inputs.append(conn)
            message[conn] = []
        else:
            # 有老用户发送信息
            try:
                date = str(sk.recv(1024), encoding="utf-8")
            except Exception as e:
                e_list.append(sk)
            else:
                if sk not in info_sender:
                    info_sender.append(sk)
                message[sk].append(date)

    for sk in w_list:
        re = message[sk][0]
        del message[sk][0]
        sk.sendall(bytes(re + 'hello', encoding="utf-8"))
        print(re)
        # 给我发送信息的对象，我回复了信息就要把它排除，不然前面有while循环，和for循环，就会不断给对方回复消息！
        info_sender.remove(sk)

    for sk in e_list:
        inputs.remove(sk)
