from select import select
from socket import *


HOST_IP = '127.0.0.1' 
err = '\033[91m'
norm = '\033[0m'
len_code = {0x0001, 0x0002, 0x0003}

def dt_request_check(packet: bytearray):
    """ check DT-request packet from client """
    if len(packet) != 6:
        print(f"{err}ERROR: Packet does not contain 6 bytes.{norm}")
    
    elif (packet[0]<<8)|packet[1] != 0x497e:
        print(f"{err}ERROR: Wrong packet received.{norm}")
    
    elif (packet[2]<<8)|packet[3] != 0x0001:
        print(f"{err}ERROR: Wrong packet type received.{norm}")
    
    elif (packet[4]<<8)|packet[5] != 0x0001 or (packet[4]<<8)|packet[5] != 0x0002:
        print(f"{err}ERROR: Unknown Request.{norm}")
    
    else:
        pass


soc_1 = socket(AF_INET, SOCK_DGRAM)
soc_1.bind(("127.0.0.1",5001))
soc_2 = socket(AF_INET, SOCK_DGRAM)
soc_2.bind(("127.0.0.1", 5002))
soc_3  = socket(AF_INET, SOCK_DGRAM)
soc_3.bind(("127.0.0.1", 5003))

soc_list = [soc_1, soc_2, soc_3]

while True:
    a, b, c = select(soc_list,[], [])
    if a[0] in soc_list:
        msg, addr = a[0].recvfrom(50000)
        dt_request_check(msg)
        

        