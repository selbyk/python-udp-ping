# UDPPingerServer.py
# We will need the following module to generate randomizedlost packets
import time
import random
from socket import *
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.settimeout(1.0)
serverSocket.bind(('127.0.0.1', 1024))
clock = int(round(time.time() * 1000))
sequence_number = 1
while sequence_number <= 10:
  clock = int(round(time.time() * 1000))
  serverSocket.sendto('PING ' + str(sequence_number) + ' ' + str(clock), ('127.0.0.1', 12000))
  # Generate random number in the range of 0 to 10 rand = random.randint(0, 10)
  # Receive the client packet along with the address it is coming from
  try:
    message, address = serverSocket.recvfrom(12000)
  except Exception,e:
    print 'Packet dropped, resending'
    continue
  print message
  last = message
  sequence_number = sequence_number + 1
