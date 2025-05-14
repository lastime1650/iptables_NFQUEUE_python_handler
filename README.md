# iptables_NFQUEUE_python_handler
iptables에서 NFQUEUE를 설정하고, 파이썬 스크립트에서 패킷을 처리하는 방법<br>
기술된 블로그: [https://blog.naver.com/lastime1650/223865102584](https://blog.naver.com/lastime1650/223865102584)

<br>

# 이게 무슨 레포지토리?

iptables에서 NFQUEUE라는 NetFilterQUEUE 라는 큐를 통하여 유저모드 환경에 패킷을 전달할 수 있습니다. 이러한 점을 통하여 Python을 통해 iptables가 NFQUEUE에 패킷을 전달할 때를 catch하여 패킷을 조작 ( DNAT과 SNAT )하는 방법을 제시하는 repo입니다.

<br>
![initial](https://github.com/lastime1650/iptables_NFQUEUE_python_handler/blob/main/nfqueue1.png)
현재 최신 iptables에서는 INVALID ( XMAS, NULL ,,, 스캔 ) 패킷을 포트포워딩한 호스트에 FORWARD를 하지않고, INPUT해버리는 문제(?)가 있어, 이를 해결하기 위해 레포지토리를 생성하였습니다.

<br>

# 구성도
![initial](https://github.com/lastime1650/iptables_NFQUEUE_python_handler/blob/main/image1.png)

패킷이 외부에서 들어올 때, mangle 테이블의 PREROUTING에서는 패킷을 FORWARD로 이동시킬 지, INPUT 시켜버릴지 결정합니다.<br><br>
이때 FORWARD를 시켜버리기 위해서는 iptables의 내부 호스트로 destination IP로 바꿔주면 ( DNAT ) FORWARD합니다. <br>
반대로, 내부 -> 외부일 때는 source IP를 밖으로 나가는 Network Interface의 주소로 변경하면 FORWARD합니다. <br>
