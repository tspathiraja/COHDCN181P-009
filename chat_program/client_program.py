#client
import sys, socket
from threading import Thread

def se():
    while True:
        da = raw_input()
        s.send(da)
    
def re():
    while True:
        DA = s.recv(1024)
        print (DA)
        
host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

t1 = Thread(target = se).start()
t2 = Thread(target = re).start()

