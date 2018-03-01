import socket

obj = socket.socket()

obj.connect(("192.168.0.100",8098))

ret_bytes = obj.recv(1024)
ret_str = str(ret_bytes.encode("utf-8"))
obj.sendall(bytes("PI1".encode("utf-8")))
print(ret_str)

while True:
    inp = raw_input("write the degree \n >>>")
    if inp == "q":
        obj.sendall(bytes(inp.encode("utf-8")))
        break
    else:
        obj.sendall(bytes(inp.encode("utf-8")))
        ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes.encode("utf-8"))
        print(ret_str)
