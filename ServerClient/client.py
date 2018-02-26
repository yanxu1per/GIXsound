import socket

obj = socket.socket()

obj.connect(("173.250.133.107",8098))

ret_bytes = obj.recv(1024)
ret_str = str(ret_bytes,encoding="utf-8")
obj.sendall(bytes("PI1",encoding="utf-8"))
print(ret_str)

while True:
    inp = input("write the degree \n >>>")
    if inp == "q":
        obj.sendall(bytes(inp,encoding="utf-8"))
        break
    else:
        obj.sendall(bytes(inp, encoding="utf-8"))
        ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes,encoding="utf-8")
        print(ret_str)
