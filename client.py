import sys
from socket import AF_INET, SOCK_DGRAM, gaierror, getaddrinfo, socket
from select import select


err = '\033[91m'
wrn = '\033[93m'
norm = '\033[0m'
len_code = {0x0001, 0x0002, 0x0003}


def dt_response_check(packet: bytearray) -> bytes:
    """ Check response from server. """

    # Check Date time response packet begins.
    if len(packet) < 13:
        print(f"{err}PACKET ERROR: Packet header does not contain 13 bytes.{norm}")
        sys.exit()
    
    # Seperate packet components here.
    mg_num = (packet[0]<<8)|packet[1]   # Magic number
    tpe = (packet[2]<<8)|packet[3]      # type of packet
    lang = (packet[4]<<8)|packet[5]     # language type
    year = (packet[6]<<8)|packet[7]     # current Year
    mnth = packet[8]                    # current Month
    day = packet[9]                     # current day
    hour = packet[10]                   # current hour
    minute = packet[11]                 # current minute
    pkt_length = packet[12]             # total length of text
    text = packet[13:]                  # actual response from server

    # Checking packet resume from here
    if mg_num != 0x497e:
        print(f"{err}PACKET ERROR: Packet does not meet Magic No requirement.{norm}")
    
    elif tpe != 0x0002:
        print(f"{err}PACKET ERROR: Packet does not meet Packet Type requirement.{norm}")
    
    elif lang not in len_code:
        print(f"{err}PACKET ERROR: Language not support.{norm}")
    
    elif year >= 2100:
        print(f"{err}PACKET ERROR: Packet header contains wrong year info.{norm}")
    
    elif mnth not in range(1, 13):
        print(f"{err}PACKET ERROR: Packet header contains wrong month info.{norm}")
    
    elif day not in range(1, 32):
        print(f"{err}PACKET ERROR: Packet header contains wrong day info.{norm}")
    
    elif hour not in range(0, 24):
        print(f"{err}PACKET ERROR: Packet header contains wrong hour info.{norm}")
    
    elif minute not in range(0, 60):
        print(f"{err}PACKET ERROR: Packet header contains wrong minute info.{norm}")
    
    elif pkt_length != len(text):
        print(f"{err}PACKET ERROR: There are missing datas in the packetheader.{norm}")

    else:
        print("MESSAGE: You've got a perfect packet!")

        return mg_num, tpe, lang, year, mnth, day, hour, minute, pkt_length, text.decode('utf-8')



soc = socket(AF_INET, SOCK_DGRAM)

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
    sys.exit()

try:
    assert 1024 <= int(sys.argv[3]) <= 64000
    addr = getaddrinfo(sys.argv[2], int(sys.argv[3]), AF_INET)[0][4]
    soc.sendto(dt_request, addr)
    rlist, wlist, exp = select([soc], [], [],1.0)
    if rlist == []:
        print(f"{wrn}FATAL: One second timed out to receive packet!{norm}")
    for sock in rlist:
        msg, addr = sock.recvfrom(50000)
        contents = dt_response_check(msg)
    
    if contents != None:
        print(f"Magic number    : {contents[0]} ({hex(contents[0])})")
        print(f"Packet Type     : {contents[1]}")
        print(f"Language Code   : {contents[2]}")
        print(f"Year            : {contents[3]}")
        print(f"Month           : {contents[4]}")
        print(f"Day             : {contents[5]}")
        print(f"Hour            : {contents[6]}")
        print(f"Minute          : {contents[7]}")
        print(f"Response Length : {contents[8]}")
        print(f"Response        : {contents[9]}")


except gaierror:
    print(f"{err}ERROR: Invalid address.{norm}")
    sys.exit()

except AssertionError:
    print(f"{err}ERROR: Invalid port number")
    sys.exit()