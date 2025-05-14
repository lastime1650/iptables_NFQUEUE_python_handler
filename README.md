# iptables_NFQUEUE_python_handler
iptables에서 NFQUEUE를 설정하고, 파이썬 스크립트에서 패킷을 처리하는 방법

<br>

# 이게 무슨 레포지토리?

iptables에서 NFQUEUE라는 NetFilterQUEUE 라는 큐를 통하여 유저모드 환경에 패킷을 전달할 수 있습니다. 이러한 점을 통하여 Python을 통해 iptables가 NFQUEUE에 패킷을 전달할 때를 catch하여 패킷을 조작 ( DNAT과 SNAT )하는 방법을 제시하는 repo입니다.

<br>

현재 최신 iptables에서는 INVALID ( XMAS, NULL ,,, 스캔 ) 패킷을 포트포워딩한 호스트에 FORWARD를 하지않고, INPUT해버리는 문제(?)가 있어, 이를 해결하기 위해 레포지토리를 생성하였습니다.

[!initial](https://github.com/lastime1650/iptables_NFQUEUE_python_handler/blob/main/image.png)
