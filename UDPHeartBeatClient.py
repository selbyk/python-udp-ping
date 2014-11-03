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
min_rtt = 0
max_rtt = 0
avg_rtt = 0
packets_dropped = 0.0
total_packets = 0.0
while sequence_number <= 10:
  clock = int(round(time.time() * 1000))
  serverSocket.sendto('PING ' + str(sequence_number) + ' ' + str(clock), ('127.0.0.1', 12000))
  total_packets = total_packets + 1
  # Generate random number in the range of 0 to 10 rand = random.randint(0, 10)
  # Receive the client packet along with the address it is coming from
  try:
    message, address = serverSocket.recvfrom(12000)
  except Exception,e:
    packets_dropped = packets_dropped + 1.0
    print 'Packet dropped, resending'
    continue
  print message
  message_time = message.split(' ')[2]
  rtt = int(round(time.time() * 1000)) - int(message_time)
  avg_rtt = avg_rtt + rtt
  if rtt < min_rtt or min_rtt == 0:
    min_rtt = rtt
  if rtt > max_rtt or max_rtt == 0:
    max_rtt = rtt
  print "RTT: " + str(rtt)
  last = message
  sequence_number = sequence_number + 1
print "Min RTT: " + str(min_rtt)
print "Max RTT: " + str(max_rtt)
print "Avg RTT: " + str(avg_rtt/10)
print "Packet Loss: " + str(packets_dropped/total_packets*100) + "%"
