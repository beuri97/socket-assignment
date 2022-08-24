""" 'client.py' starts here. """

import sys
from socket import AF_INET, SOCK_DGRAM, gaierror, getaddrinfo, socket
from select import select

# Coloring Print message
err = '\033[91m'
wrn = '\033[93m'
norm = '\033[0m'
# Set of language code to check packet.
lang_code = {0x0001, 0x0002, 0x0003}


def dt_response_check(packet: bytearray) -> tuple:
    """ Check response from server. """

    # Check Date time response packet begins.
    if len(packet) < 13:
        print(f"{err}PACKET ERROR: Packet header does not contain 13 bytes.{norm}")
        sys.exit()
    
    # Seperate packet components here.
    mg_num = (packet[0] << 8) | packet[1]   # Magic number
    pkt_type = (packet[2] << 8) | packet[3] # type of packet
    lang = (packet[4] << 8) | packet[5]     # language type
    year = (packet[6] << 8) | packet[7]     # current Year
    mnth = packet[8]                        # current Month
    day = packet[9]                         # current day
    hour = packet[10]                       # current hour
    minute = packet[11]                     # current minute
    pkt_length = packet[12]                 # text length
    text = packet[13:]                      # actual response

    # Checking packet resume from here
    if mg_num != 0x497e:
        print(f"{err}PACKET ERROR: Packet does not meet Magic No requirement.{norm}")
    
    elif pkt_type != 0x0002:
        print(f"{err}PACKET ERROR: Packet does not meet Packet Type requirement.{norm}")
    
    elif lang not in lang_code:
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
        content = (mg_num, pkt_type, lang, year, mnth, day, hour, minute, pkt_length, text.decode('utf-8'))

        return content


def client():
    """ main client """

    if len(sys.argv) < 4:
        print(f"{err}ERROR: you missing requirement(Either request type, address, or port){norm}")
        sys.exit()
    
    sokt = socket(AF_INET, SOCK_DGRAM)

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
        sokt.sendto(dt_request, addr)
        socket_list, empty_list, except_list = select([sokt], [], [], 1.0)
        if len(socket_list) == 0:
            raise RuntimeError

        for sock in socket_list:
            msg, addr = sock.recvfrom(50000)
            content = dt_response_check(msg)
        
        if content != None:
            print(f"Magic number    : {content[0]}")
            print(f"Packet Type     : {content[1]}")
            print(f"Language Code   : {content[2]}")
            print(f"Year            : {content[3]}")
            print(f"Month           : {content[4]}")
            print(f"Day             : {content[5]}")
            print(f"Hour            : {content[6]}")
            print(f"Minute          : {content[7]}")
            print(f"Response Length : {content[8]}")
            print(f"Response        : {content[9]}")


    except gaierror:
        print(f"{err}ERROR: Invalid address.{norm}")

    except AssertionError:
        print(f"{err}ERROR: Invalid port number")

    except RuntimeError:
        print(f"{wrn}FATAL: One second exceed to receive packet!{norm}")

if __name__ == '__main__':
    client()

""" 'client.py' ends here. """