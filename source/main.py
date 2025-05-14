#!/usr/bin/env python3

from scapy.all import IP, TCP, Raw, Ether, wrpcap
from netfilterqueue import NetfilterQueue
import os
import socket
import struct
import binascii


def handle_packet(pkt):
    print(pkt)
    
    pkt.get_payload()
    
    Original_Packet_Binary:bytes = pkt.get_payload()
    
    # TCP 체크
    IP_packet = IP(Original_Packet_Binary)
    if IP_packet.haslayer("IP"):
        
        TCP_packet = IP_packet["TCP"]
        
        if ( str(IP_packet["IP"].dst) == "192.168.220.1" ):
            # DNAT

            # Ex -> In
            print( "DNAT ..\n " + IP_packet.dst ) # 변경 전
        
            IP_packet["IP"].dst = "10.0.3.10" # 하드코딩,,,, 
            print( IP_packet.dst ) # 변경 후

        elif ( str(IP_packet["IP"].src) == "10.0.3.10" ):

            # SNAT
            
            # Internal ==> External
            print( "SNAT .. \n" + IP_packet.src ) # Before

            IP_packet["IP"].src = "192.168.220.1"

            print( IP_packet.src ) # After 
        



        # 패킷 바이너리가 달라졌기에,, 체크섬 무결성 값은 깨짐
        # 삭제!

        del IP_packet["IP"].chksum
        del TCP_packet.chksum
        
        pkt.set_mark(1234) # 마크 적용 -> iptables - POSTROUTING에서 이를 확인할 것
        
        pkt.set_payload( bytes(IP_packet) ) # 실제 패킷까지 적용 하기
        
        
        
    pkt.accept()
    return 

QUEUE_NUM = 0

nfqueue = NetfilterQueue()
nfqueue.bind(
    QUEUE_NUM,
    handle_packet
)
nfqueue.run()

'''

사전으로 해야하는 작업은 다음과 같습니다.

1) dnf install libnetfilter_queue libnetfilter_queue-devel python3 python3-pip gcc make python3-devel -y
* redhat 계열

2) pip3 install NetfilterQueue scapy

3) (외부 -> 내부 패킷올 때 NFQUEUE 규칙) iptables에서 -t mangle -I PREROUTING /*... */ -j NFQUEUE --queue-num 0 <- 큐 넘버는 0으로 가정
4) (내부 -> 외부 패킷올 때 NFQUEUE 규칙) iptables에서 -t mangle -I POSTROUTING /*... */ -j NFQUEUE --queue-num 0 <- 큐 넘버는 0으로 가정

'''
