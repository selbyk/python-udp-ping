# UDPPingClient.py
import time
from socket import *

# What's your IP address and witch port should we use?
recieve_host = '127.0.0.1'
recieve_port = 1024

# What's the remote host's IP address and witch port should we use?
remote_host = '127.0.0.1'
remote_port = 12000

# number of times to ping
num_pings = 10

# Keep track of some things
sequence_number = 1
min_rtt = 0
max_rtt = 0
avg_rtt = 0
packets_dropped = 0.0
total_packets = 0.0

# Setup a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.settimeout(1.0)
serverSocket.bind((recieve_host, recieve_port))

def get_time():
  return int(round(time.time() * 1000))

def wait_for_response():
  global packets_dropped
  while True:
    # Generate random number in the range of 0 to 10 rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    try:
      message, address = serverSocket.recvfrom(remote_port)
      return message
    except Exception,e:
      packets_dropped = packets_dropped + 1
      return 'ERROR 522 ' + str(get_time()) + ' TIMEOUT'

def send_message(message,wait=False):
   serverSocket.sendto(message, (remote_host, remote_port))
   if wait == False:
     return
   else:
     return wait_for_response()

while sequence_number <= num_pings:
  # Create message with current sequence_number and time
  message = 'PING ' + str(sequence_number) + ' ' + str(get_time())
  # Recieve ping
  recieved = send_message(message, True)
  recieved_size = len(recieved)
  recieved_array = recieved.split(' ')
  recieved_type = recieved_array[0].upper()
  #print recieved_type
  recieved_seq = int(recieved_array[1])
  recieved_time = int(recieved_array[2])
  #print recieved_time
  rtt = get_time() - recieved_time
  if rtt > 1000:
    continue
  if recieved_type == 'PING':
    print str(recieved_size) + " bytes recieved from " + remote_host + ':' + str(remote_port) + ': seq=' + str(recieved_seq) + ' rtt=' + str(rtt)
    avg_rtt = avg_rtt + rtt
    if rtt < min_rtt or min_rtt == 0:
      min_rtt = rtt
    if rtt > max_rtt or max_rtt == 0:
      max_rtt = rtt
    sequence_number = sequence_number + 1
  elif recieved_type == 'ERROR':
    recieved_message = recieved_array[3]
    print recieved
  else:
    print 'Something went wrong, but I have no idea what it is.'
  last = recieved

  total_packets = total_packets + 1
# Out of the loop, report running statistics
print "RTT: min=" + str(min_rtt) + " max=" + str(max_rtt) + " avg=" + str(avg_rtt/10)
print "Packet Loss: " + str(packets_dropped/total_packets*100) + "%"
