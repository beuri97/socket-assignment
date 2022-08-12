import socket


HOST_IP = '127.0.0.1' 
err = '\033[91m'
norm = '\033[0m'
len_code = {0x0001, 0x0002, 0x0003}

# def dt_request_check(packet: bytearray):
#     """ check DT-request packet from client """
#     if len(packet) != 6:
#         print(f"{err}ERROR: Packet does not contain 6 bytes.{norm}")
    
#     elif (packet[0]<<8)|packet[1] != 0x497e:
#         print(f"{err}ERROR: Wrong packet received.{norm}")
    
#     elif (packet[2]<<8)|packet[3] != 0x0001:
#         print(f"{err}ERROR: Wrong packet type received.{norm}")
    
#     elif (packet[4]<<8)|packet[5] != 0x0001 or (packet[4]<<8)|packet[5] != 0x0002:
#         print(f"{err}ERROR: Unknown Request.{norm}")
    
#     else:
#         pass

def dt_response_check(packet: bytearray):
    """ Check response from server. """
    if len(packet) != 13:
        print(f"{err}PACKET ERROR: Packet does not contain 13 bytes.{norm}")
    
    elif (packet[0]<<8)|packet[1] != 0x497e:
        print(f"{err}PACKET ERROR: Packet does not meet key requirement.{norm}")
    
    elif (packet[2]<<8)|packet[3] != 0x0002:
        print(f"{err}PACKET ERROR: Packet does not meet its requirement.{norm}")
    
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
    
    elif packet[12] != (32*3)+8:
        print(f"{err}PACKET ERROR: There are missing datas in the packetheader.{norm}")

    else:
        pass
