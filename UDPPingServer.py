# UDPPingServer.py
# We will need the following module to generate randomizedlost packets
import random
from socket import *
import time

# What's your IP address and witch port should we use?
recieve_host = '127.0.0.1'
recieve_port = 12000

# What's the remote host's IP address and witch port should we use?
remote_host = '127.0.0.1'
remote_port = 1024

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind((recieve_host, recieve_port))

simulate_packet_loss = True
sleep_for_rand_response_times = True

def get_time():
  return int(round(time.time() * 1000))

def send_message(message,wait=False):
   serverSocket.sendto(message, (remote_host, remote_port))
   if wait == False:
     return
   else:
     return wait_for_response()

# Just respond to ping requests
while True:
  # Receive the client packet along with the address it is coming from
  message, address = serverSocket.recvfrom(remote_port)
  # Capitalize the message from the client
  message = message.upper()
  print 'Recieve: ' + message
  # If rand is less is than 4, we consider the packet lost and do not respond
  if sleep_for_rand_response_times:
    min_sleep = 0.2
    max_sleep = 1.0
    time.sleep(random.uniform(min_sleep, max_sleep))
    if simulate_packet_loss:
      if random.randint(0, 10) < 2:
        print 'Dropped, lol'
        continue
  elif simulate_packet_loss:
    if random.randint(0, 10) < 4:
      print 'Dropped, lol'
      continue
  serverSocket.sendto(message, address)
  print 'Send: ' + message
