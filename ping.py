import os, sys, socket, struct, time
ICMP_ECHO_REQUEST = 8

def chksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        a = ord(msg[i]) 
        b = ord(msg[i+1])
        s = s + (a+(b << 8))
    s = s + (s >> 16)
    s = ~s & 0xffff
    return s

for z in range (1,5):
    dest_addr = sys.argv[1]
    icmp_seq = z
    sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, 124,icmp_seq)
    icmp_h = chksum(header)
    header2 = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, icmp_h, 124, icmp_seq)
    sen = time.time()
    sock.sendto(header2, (dest_addr,1))  

    pkt, addr = sock.recvfrom(1024)
    come = time.time()
    ipv4Header = pkt[:20]
    icmpHeader = pkt[20:28]
    ver, ttl, proto, chk, src, drc = struct.unpack('!B 7x B B H 4s 4s', ipv4Header)
    typ, code, checksum, packetID, sequence = struct.unpack("!bbHHh", icmpHeader)
    last_time = ('%.3f'%((come - sen) * 1000))
    
    if typ == 0:
        print('from {0}: icmp_seq={1} ttl={2} time={3}ms'.format(socket.inet_ntoa(src), icmpseq, ttl, last_time))
    elif typ == 3:
        print('From {0}: icmp_seq={1} {2}'.format(socket.inet_ntoa(drc), z, 'Destination Host Unreachable'))
    time.sleep(1)

