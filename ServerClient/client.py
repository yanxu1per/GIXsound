import socket  
addr = ('69.91.160.215',10000)  
readdr = ('173.250.145.152',12000) 
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
  
s.bind(readdr)  
while 1:  
    
    data = raw_input("input:")
    
    if not data:  
        break  
    s.sendto(unicode(data,'utf-8'),addr)  
  
    recivedata,addrg = s.recvfrom(2048)  
    if recivedata:  
        print("from:",addrg)  
        print("got recive :",recivedata.decode())  
s.close()  
