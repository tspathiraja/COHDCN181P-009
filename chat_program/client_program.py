#client
import sys, socket
from threading import Thread

def se():
    while True:
        da = raw_input()
        s.send(da)

try:
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    t1 = Thread(target = se)
    t1.daemon = True
    t1.start()

except KeyboardInterrupt:
        s.close()
        sys.exit()

while True:
    try:
        DA = s.recv(1024)
        print (DA)

    except KeyboardInterrupt:
        s.close()
        sys.exit()

    else:
        if not DA:
            break

