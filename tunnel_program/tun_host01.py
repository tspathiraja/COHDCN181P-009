#########################################
#   create TUN interface command        #   
#########################################
#sudo ip tuntap add dev asa0 mode tun   #
#sudo ip addr add 10.0.1.1/24 dev asa0  #
#sudo ip link set dev asa0 up           #
#ip addr show                           #
#########################################

import fcntl,threading,os,struct,subprocess,socket,sys
from struct import *

TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

def chksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        a = ord(msg[i])
        b = ord(msg[i+1])
        s = s + (a+(b << 8))
    s = s + (s >> 16)
    s = ~s & 0xffff
    return s

# Open TUN device file.
tun = open('/dev/net/tun', 'r+b')
# Tall it we want a TUN device named tun0.
ifr = struct.pack('16sH', 'asa0', IFF_TUN | IFF_NO_PI)
fcntl.ioctl(tun, TUNSETIFF, ifr)
# Optionally, we want it be accessed by the normal user.
fcntl.ioctl(tun, TUNSETOWNER, 1000)
# Bring it up and assign addresses.
subprocess.check_call('ifconfig asa0 10.0.1.1 pointopoint 10.0.1.2 up', shell=True)

recv_sock = socket.socket(socket.AF_PACKET,socket.SOCK_RAW, socket.htons(0x0800))
send_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW)

try:
    while True:
        recv_packet =str(os.read(tun.fileno(), 2048))
        send_sock.sendto(recv_packet,("192.168.137.32",0))

except KeyboardInterrupt :
    print ("Closed!")
