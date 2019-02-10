from socket import *

CLIENT_SOCKET = ('', 13373)
SERVER_SOCKET = ('', 1337)

def recieve():
  cs = socket(AF_INET, SOCK_DGRAM)
  cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
  cs.bind(CLIENT_SOCKET)
  data, addr = cs.recvfrom(1024)
  data = data.decode()
  return [int(bit) for bit in data]

def transmit(raw):
  ss = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
  ss.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
  ss.settimeout(0.2)
  ss.bind(SERVER_SOCKET)
  ss.sendto(''.join(map(str, raw)).encode(), ('<broadcast>', CLIENT_SOCKET[1]))
