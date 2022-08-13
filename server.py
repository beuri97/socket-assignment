from select import select
from socket import *

soc_1 = socket(AF_INET, SOCK_DGRAM)
soc_1.bind(("127.0.0.1",5001))
soc_2 = socket(AF_INET, SOCK_DGRAM)
soc_2.bind(("127.0.0.1", 5002))
soc_3  = socket(AF_INET, SOCK_DGRAM)
soc_3.bind(("127.0.0.1", 5003))

soc_list = [soc_1, soc_2, soc_3]

while True:
    a, b, c = select(soc_list,[], [])
    print(a, b, c)
    if a[0] == soc_1:
        msg, addr = a[0].recvfrom(50000)
        print(f"Hi client from {addr}. This is port 5001")
    elif a[0] == soc_2:
        msg, addr = a[0].recvfrom(50000)
        print(f"Hi client from {addr}. This is port 5002")
    elif a[0] == soc_3:
        msg, addr = a[0].recvfrom(50000)
        print(f"Hi client from {addr}. This is port 5003")