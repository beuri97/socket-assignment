from select import select
from socket import *
from time import localtime, strftime
import os


err = '\033[91m'
norm = '\033[0m'
len_code = {0x0001, 0x0002, 0x0003}

def dt_request(packet: bytearray) -> tuple:
    """ check DT-request packet from client and generate packet to send back to client """
   
    if len(packet) != 6:
        print(f"{err}ERROR: Packet does not contain 6 bytes.{norm}")
    
    elif (packet[0]<<8)|packet[1] != 0x497e:
        print(f"{err}ERROR: Wrong packet received.{norm}")
    
    elif (packet[2]<<8)|packet[3] != 0x0001:
        print(f"{err}ERROR: Wrong packet type received.{norm}")
    
    elif (packet[4]<<8)|packet[5] >= 2:
        print(f"{err}ERROR: Unknown Request.{norm}")
    
    else:
        print("MESSAGE: Server got package on: ", end = ' ')
        mg_num = 0x497E
        pak_type = 0x0002
        year_now = strftime("%Y", localtime())
        month_now = strftime("%m", localtime())
        day_now = strftime("%d", localtime())
        hour_now = strftime("%H", localtime())
        min_now = strftime("%M", localtime())

        if addr[1] == 5001 and (packet[4]<<8)|packet[5] == 0x0001:          # Date in English
            l_code = 0x0001
            pay_load = f"Today's date is {month_now} {day_now}, {year_now}"
            pay_load = bytes(pay_load, encoding='utf-8')
        
        elif addr[1] == 5001 and (packet[4]<<8)|packet[5] == 0x0002:        # Time in English
            l_code = 0x0001
            pay_load = f"The current time is {hour_now}:{min_now}"
            pay_load = bytes(pay_load, encoding='utf-8')

        if addr[1] == 5002 and (packet[4]<<8)|packet[5] == 0x0001:          # Date in Te reo Maori
            l_code = 0x0002
       
        elif addr[1] == 5002 and (packet[4]<<8)|packet[5] == 0x0002:        # Time in Te reo Maori
            l_code = 0x0002

        if addr[1] == 5003:     
            l_code = 0x0003

        # DT-Response packet generate begins.
        # new_packet = bytearray(12)
        # new_packet[0] = mg_num >> 8
        # new_packet[1] = mg_num & 0xFF
        # new_packet[2] = 0x00
        # new_packet[3] = pak_type
        # new_packet[4] = 0x00
        # new_packet[5] = l_code
        # new_packet[6] = year_now >> 8
        # new_packet[7] = year_now & 0xFF
        # new_packet[8] = month_now
        # new_packet[9] = day_now
        # new_packet[10] = hour_now
        # new_packet[11] = min_now
        # new_packet[12] = len(pay_load)
        # new_packet += pay_load

        return 


soc_1 = socket(AF_INET, SOCK_DGRAM)
soc_1.bind(('',5001))
soc_2 = socket(AF_INET, SOCK_DGRAM)
soc_2.bind(('',5002))
soc_3  = socket(AF_INET, SOCK_DGRAM)
soc_3.bind(('',5003))

soc_list = [soc_1, soc_2, soc_3]

while True:
    a, b, c = select(soc_list,[], [])
    if a[0] in soc_list:
        msg, addr = a[0].recvfrom(50000)
        print(f"I got {addr} packet")
        print(msg)
        new_msg = dt_request(msg)
        a[0].sendto(new_msg, addr)
        a[0].close()