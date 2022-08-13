import sys
from socket import AF_INET, SOCK_DGRAM, gethostname, socket
from select import select

soc = socket(AF_INET, SOCK_DGRAM)
soc.bind((gethostname(), 64000))

type(sys.argv[1])

soc.sendto(b"Hola", ("127.0.0.1", int(sys.argv[1])))
soc.close()