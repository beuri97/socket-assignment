import sys
from socket import AF_INET, SOCK_DGRAM, gethostbyname_ex, gethostname, socket
from select import select

HOST = gethostbyname_ex(gethostname())[2][1]
soc = socket(AF_INET, SOCK_DGRAM)
soc.bind((HOST, 7777))


soc.sendto(b'Hello?', (sys.argv[1], int(sys.argv[2])))
soc.close()