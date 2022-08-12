import sys
from socket import AF_INET, SOCK_DGRAM, gethostname, socket
from select import select

soc = socket(AF_INET, SOCK_DGRAM)
soc.bind((gethostname(), 6974))

for port in sys.argv[1:]:
    pass