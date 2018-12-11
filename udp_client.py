import socket
import threading
import time

key = 8194

shutdown = False
join = False


# def receving(name, sock):
#     while not shutdown:
#         try:
#             while True:
#                 data, addr = sock.recvfrom(1024)

#                 decrypt = ''
#                 k = False
#         except:
#             pass

alias = input('Name: ')

while not shutdown:
    if not join:
        s.sendto(f'[{alias}] <= join'.encode('utf-8'))
