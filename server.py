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
    for d in a:
        msg, addr = d.recvfrom(5000)
        print(msg ,addr)
        d.close()