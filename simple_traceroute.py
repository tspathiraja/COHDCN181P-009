import sys, socket, struct, time

port=80
ttl=1
max_hops=30
dest_name=sys.argv[1]
dest_addr=socket.gethostbyname(dest_name)
print("traceroute to {0} ({1}), 30 hops max".format(dest_name,dest_addr))

while True:
    recv_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    send_socke = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    send_socke.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    recv_sock.settimeout(2)
    recv_sock.bind(("",port))
    print(ttl),
    
    send_time=time.time()
    send_socke.sendto("",(dest_addr,port))
    
    ne_addr=None
    ne_name=None
    total=None
    complete=False
    step=3
    
    while not complete and step>0:
        try:
            rec, addr = recv_sock.recvfrom(1024)
            recv_time=time.time()
            complete=True
            ne_addr = addr[0]
            try:
                ne_name=socket.gethostbyaddr(ne_addr)[0]
            except socket.error:
                ne_name = ne_addr
        except socket.error:
            step=step-1
            print("* "),
    
    recv_sock.close()
    send_socke.close()

    if not complete:
        pass

    if ne_addr is not None:
        ne_host = "%s (%s)" % (ne_name, ne_addr)
        total=('%.3f'%((recv_time-send_time) * 1000))
        tim="%s ms" %total
        print('{0} {1}'.format(ne_host,tim))
    else:
        ne_host = ""
        total = ""
        print('{0} {1}'.format(ne_host,total))
    
    ttl=ttl+1    
    if ne_addr == dest_addr or ttl>30:
        break

