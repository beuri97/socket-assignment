import sys
from socket import AF_INET, SOCK_DGRAM, gethostname, socket
from select import select

server = sys.argv[1]
soc = socket(AF_INET, SOCK_DGRAM)
soc.bind(("", 64000))

soc.sendto(b"Hola", (server, int(sys.argv[2])))
soc.close()