import socket  
address = ('127.0.0.1',10000)#local  
readdr = ("127.0.0.1",12000)#client 
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
  
s.bind(address)  
while 1:  
    data,addr=s.recvfrom(2048)  
    if not data:  
        break  
    print("got data from",addr)  
    print(data.decode())  
    replydata = input("reply:")  
    s.sendto(replydata.encode("utf-8"),readdr)  
s.close()  