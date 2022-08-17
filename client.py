import sys
from socket import AF_INET, SOCK_DGRAM, getaddrinfo, socket
from select import select


err = '\033[91m'
wrn = '\033[93m'
norm = '\033[0m'
len_code = {0x0001, 0x0002, 0x0003}

def dt_response_check(packet: bytearray) -> bytes:
    """ Check response from server. """

    if len(packet) < 13:
        print(f"{err}PACKET ERROR: Packet header does not contain 13 bytes.{norm}")
        return  #need to terminate this function immidiately if packet header does not meet requirement.
    
    text = packet[13:]
    if (packet[0]<<8)|packet[1] != 0x497e:
        print(f"{err}PACKET ERROR: Packet does not meet Magic No requirement.{norm}")
    
    elif (packet[2]<<8)|packet[3] != 0x0002:
        print(f"{err}PACKET ERROR: Packet does not meet Packet Type requirement.{norm}")
    
    elif (packet[4]<<8)|packet[5] not in len_code:
        print(f"{err}PACKET ERROR: Language not support.{norm}")
    
    elif (packet[6]<<8)|packet[7] >= 2100:
        print(f"{err}PACKET ERROR: Packet header contains wrong year info.{norm}")
    
    elif packet[8] not in range(1, 13):
        print(f"{err}PACKET ERROR: Packet header contains wrong month info.{norm}")
    
    elif packet[9] not in range(1, 32):
        print(f"{err}PACKET ERROR: Packet header contains wrong day info.{norm}")
    
    elif packet[10] not in range(0, 24):
        print(f"{err}PACKET ERROR: Packet header contains wrong hour info.{norm}")
    
    elif packet[11] not in range(0, 60):
        print(f"{err}PACKET ERROR: Packet header contains wrong minute info.{norm}")
    
    elif packet[12] != len(text):
        print(f"{err}PACKET ERROR: There are missing datas in the packetheader.{norm}")

    else:
        print("MESSAGE: You've got a perfect packet!")
        
        return text



soc = socket(AF_INET, SOCK_DGRAM)
soc.bind(('', 7777))

dt_request = bytearray(6)
dt_request[0] = 0x497E >> 8
dt_request[1] = 0x497E & 0xFF
dt_request[2] = 0x00
dt_request[3] = 0x0001
dt_request[4] = 0x00
if sys.argv[1].lower() == 'date':
    dt_request[5] = 0x01

elif sys.argv[1].lower() == 'time':
    dt_request[5] = 0x02

else:
    print(f"{err}REQUEST ERROR: Unknown Request Type.{norm}")


addr = getaddrinfo(sys.argv[2], int(sys.argv[3]), AF_INET)[0][4]
soc.sendto(dt_request, addr)
rlist, wlist, exp = select([soc], [], [],1.0)
if rlist == []:
    print(f"{wrn}FATAL: One second timed out to receive packet!{norm}")
for sock in rlist:
    msg, addr = sock.recvfrom(50000)
    text = dt_response_check(msg)

    if msg != None:
        text = text.decode(encoding='utf-8')
        print(text)