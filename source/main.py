#!/usr/bin/env python3

from scapy.all import IP, TCP, Raw, Ether, wrpcap
from netfilterqueue import NetfilterQueue
import os
import socket
import struct
import binascii


def handle_packet(pkt):# 핸들러
    print(pkt)
    
    pkt.get_payload()
    
    Original_Packet_Binary:bytes = pkt.get_payload()
    
    # TCP 체크
    IP_packet = IP(Original_Packet_Binary)
    if IP_packet.haslayer("IP"): # IP인가? 
        
        TCP_packet = IP_packet["TCP"] # TCP 추출 -> 이 경우, if문으로 적절하게 확인하는 것을 추천합니다.
        
        if ( str(IP_packet["IP"].dst) == "192.168.220.1" ):
            # DNAT

            # Ex -> In
            print( "DNAT ..\n " + IP_packet.dst ) # 변경 전
        
            IP_packet["IP"].dst = "10.0.3.10" # 하드코딩,,,,  ( 10.0.3.10 은 현재 포트포워딩된 내부 호스트 IP입니다. )
            print( IP_packet.dst ) # 변경 후

        elif ( str(IP_packet["IP"].src) == "10.0.3.10" ):

            # SNAT
            
            # Internal ==> External
            print( "SNAT .. \n" + IP_packet.src ) # Before

            IP_packet["IP"].src = "192.168.220.1" # ( 192.168.220.1 은 외부 통신 네트워크 인터페이스에 할당된 IP입니다. )

            print( IP_packet.src ) # After 
        



        # 패킷 바이너리가 달라졌기에,, 체크섬 무결성 값은 깨짐
        # 삭제하고, bytes()시 체크섬을 다시 구함

        del IP_packet["IP"].chksum 
        del TCP_packet.chksum
        
        pkt.set_payload( bytes(IP_packet) ) # 바이너리 변환(체크섬  다시구함 ) set_payload로 변경사항 적용
        
        
        
    pkt.accept() # 다시 iptables로 패킷 복귀
    return 

QUEUE_NUM = 0 # NFQUEUE --queue-num 0 일 때

nfqueue = NetfilterQueue()
nfqueue.bind(
    QUEUE_NUM, # NFQUEUE 큐 넘버
    handle_packet # 핸들러 함수
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
