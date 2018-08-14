#server
import sys, socket
from threading import Thread

def SE():
    while True:
        data = raw_input()
        c.send(data)
    
def RE():
    while True:
        DATA = c.recv(1024)
        print (DATA)
            
host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)
c, addr = s.accept()

T1 = Thread(target = SE).start()
T2 = Thread(target = RE).start()


