import socket

TCP_IP = '129.241.187.118'
TCP_PORT = 6000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def sendMessage(mess):
    MESSAGE = mess
    s.sendto(str(MESSAGE) + "\n",(TCP_IP,TCP_PORT))
