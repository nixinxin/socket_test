import socket

def shuru():
    sk1 = socket.socket()
    sk1.connect(("localhost", 1234))
    while True:
        content1 = str(sk1.recv(1024), encoding="utf-8")
        a = []
        print(content1)
        inp = "1234"
        if inp == "q":
            a.append(inp)
            break
        else:
            sk1.sendall(bytes(inp, encoding="utf-8"))
            content2 = str(sk1.recv(1024), encoding="utf-8")
            print(content2)
        if a == ["q"]:
            break
    sk1.close()


if __name__ == '__main__':
    # shuru()
    import logging
    logging.info('123')