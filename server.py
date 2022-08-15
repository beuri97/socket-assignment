from calendar import month
from select import select
from socket import *
from datetime import datetime


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

HOST = gethostbyname_ex(gethostname())[2][1]
soc_1 = socket(AF_INET, SOCK_DGRAM)
soc_1.bind((HOST,5001))
soc_2 = socket(AF_INET, SOCK_DGRAM)
soc_2.bind((HOST,5002))
soc_3  = socket(AF_INET, SOCK_DGRAM)
soc_3.bind((HOST,5003))

soc_list = [soc_1, soc_2, soc_3]

while True:
    a, b, c = select(soc_list,[], [])
    if a[0] not in soc_list:
        print(f"{err}ERROR: Looks like we got wrong packet.{norm}")
    else:
        msg, addr = a[0].recvfrom(50000)
        print(f"I got {addr} packet")
        dt_request_check(msg)
        
        current = datetime.now()

        mg_num = 0x497E
        pak_type = 0x0002

        if addr[1] == 5001:
            l_code = 0x0001

        elif addr[1] == 5002:
            l_code = 0x0002

        elif addr[1] == 5003:
            l_code = 0x0003

        year_now = current.strftime("%Y")
        month_now = current.strftime("%m")
        day_now = current.strftime("%d")
        hour_now = current.strftime("%H")
        min_now = current.strftime("%M")
        