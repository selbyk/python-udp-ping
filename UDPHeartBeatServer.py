# UDPHeartBeatServer.py
# We will need the following module to generate randomizedlost packets
import random
from socket import *
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 12000))
sequence_num = 0
message_time = 0
while True:
  clock = int(round(time.time() * 1000))
  # assume disconnect if it takes more than 2.5s for another heartbeat
  if message_time != 0 and clock > message_time + 2500:
    print "Client disconnected"
    sequence_num = 0
    message_time = 0
    continue
  # Generate random number in the range of 0 to 10
  rand = random.randint(0, 10)
  # Receive the client packet along with the address it is coming from
  message, address = serverSocket.recvfrom(1024)
  # Capitalize the message from the client
  message = message.upper()
  message_split = message.split(' ')
  recieved_message_time = message_split[2]
  recieved_sequence_num = message_split[1]
  if message_time != 0:
    print "Time difference: " + str(recieved_message_time)
  if recieved_sequence_num != sequence_num + 1 and sequence_num != 0:
    print "Lost " + str(recieved_sequence_num-sequence_num)