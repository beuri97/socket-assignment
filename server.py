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
    select(soc_list,[], [])
    msg_1, addr_1 = soc_1.recvfrom(2048)
    msg_2, addr_2 = soc_2.recvfrom(2048)
    msg_3, addr_3 = soc_3.recvfrom(2048)
    if msg_1 != None or addr_1 != None:
        print("Hello client1(5001)")
    elif msg_2 != None or addr_2 != None:
        print("Hello client2(5002)")
    elif msg_3 != None or addr_3 != None:
        print("Hello client3(5003)")