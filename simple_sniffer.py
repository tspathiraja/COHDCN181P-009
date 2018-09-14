from ctypes import *
import socket, struct

def main():
    eth_proto_all = 0x0003
    sock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(eth_proto_all))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('ens32', 0))

    while True:
        data, addr = sock.recvfrom(65565)
        (drc_m, src_m, proto_m, data) = ethernet(data)
        print ('>>>Ethernet')
        print ('\tdestination: {}, source: {}, protocol: {}'.format(drc_m, src_m, proto_m))

        (version, header_length, ttl, proto, chk, drc, src, data) = ipv4(data)
        print ('>>> Ipv4')
        print ('\tversion: {}, header length: {}, TTL: {}, Checksum: {}'.format(version, header_length, ttl, chk))
        print ('\tdestination ip: {}, source ip: {}'.format(drc, src))
        
        if proto == 1:
            (icmp_type, code, chksum, data) = icmp(data)
            print ('>>>ICMP Packet:')
            print ('\tType: {}, Code: {}, Checksum: {},'.format(icmp_type, code, chksum))
            print ('\n')
        elif proto == 6:
            (src_po, drc_po, sequ, ack, data) = tcp(data)
            print ('>>>TCP')
            print ('\tdestination port: {}, source port: {}, Sequence: {}, Acknowledgment: {}'.format(drc_po,src_po,sequ,ack))
            print ('\n')
        elif proto == 17:
            src_p, drc_p, size = udp(data)
            print ('>>>UDP')
            print ('\tSource Port: {}, Destination Port: {}, Length: {}'.format(src_p, drc_p, size))
            print ('\n')


def ethernet(data):
    drc_m, src_m, proto_m = struct.unpack('!6s6sH', data[:14])
    return mac_addr(drc_m), mac_addr(src_m), socket.htons(proto_m), data[14:]

def mac_addr(mac):
    li=[]
    for i in mac:
        li.append('%02x'%ord(i))
    return ":".join(li).upper()


def ipv4(data):
    ver, ttl, proto, chk, src, drc = struct.unpack('!B 7x B B H 4s 4s', data[:20])
    version = ver >> 4
    header_length = ver & 15
    return version, header_length, ttl, proto, chk, ip(src), ip(drc), data[header_length:]

def ip(addr):
    IP = socket.inet_ntoa(addr)
    return IP

def icmp(data):
    icmp_type, code, chksum = struct.unpack('!B B H', data[:4])
    return icmp_type, code, chksum, data[4:]

def tcp(data):
    src_po, drc_po, sequ, ack, offset_flag = struct.unpack('!H H L L H', data[:14])
    offset = offset_flag >> 12
    return src_po, drc_po, sequ, ack, data[offset:]

def udp(data):
    src_p, drc_p, size = struct.unpack('! H H 2x H',data[:8])
    return  src_p, drc_p, size

main ()
