from select import select
from socket import *

soc_1 = socket(AF_INET, SOCK_DGRAM)
soc_1.bind("",5001)
