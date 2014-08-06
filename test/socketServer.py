import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print>>sys.stderr,'starting up on%s port%s'% server_address
sock.bind(server_address)
sock.settimeout(2.0)

while True:
    try:
        print>>sys.stderr,'\nwaiting to receive message'
        data, address = sock.recvfrom(4096)
        print>>sys.stderr,'received %s bytes from %s'% \
            (len(data), address)
        print>>sys.stderr, data
        if data:
            sent = sock.sendto(data, address)
            print>>sys.stderr,'sent%s bytes back to%s'% \
                (sent, address)
    except Exception, e:
        print e 
