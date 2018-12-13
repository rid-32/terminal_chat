# Здесь клиент - это тоже сервер, т.е. клиент тоже создаёт сокет, и уже 2 сокета
# общаются между собой.

# Можно ли для UDP сделать так же, как сделано  для TCP ?

import socket
import threading
import time
import sys

if len(sys.argv) != 3:
    print('Usage: script, IP address, port number')
    exit()

try:
    alias = str(input('Name: '))
except:
    print('\n[ Goodbye ]')
    exit()

server_host = str(sys.argv[1])
server_port = int(sys.argv[2])

server_addr = (server_host, server_port)

# клиент всегда запущен на локальной машине
# порт будет выбран автоматически
client_host = '127.0.0.1'
client_port = 0

client_addr = (client_host, client_port)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(client_addr)
# client.setblocking(0)

key = 8194

shutdown = False
# флаг того, подключен ли клиент к серверу или нет, т.е. отправлял ли клиент
# серверу какминимум одно сообщение.
# Здесь нет такого понятия, как connect. Но соединение всё-таки устанавливается
join = False


def receving(name, sock):
    ''' приём данных от сервера осуществляется в отдельном потоке '''
    shutdownThread = False

    while not shutdownThread:
        try:
            data, addr = sock.recvfrom(1024)

            print(data.decode('utf-8'))

            time.sleep(0.2)
        except:
            print('\n Goodbye')
            shutdownThread = True


recvThread = threading.Thread(target=receving, args=('RecvThread', client))
recvThread.start()

# в основном потоке осуществляется отправка введённых данных на сервер
while not shutdown:
    try:
        # если клиент только что подключился, то нужно отправить соощение с именем
        if not join:
            client.sendto(f'[{alias}] => join to the chatroom'.encode(
                'utf-8'), server_addr)
            join = True

        message = str(input())

        if message != '':
            msg = f'[{alias}] :: {message}'
            client.sendto(msg.encode('utf-8'), server_addr)
    except:
        client.sendto(f'[{alias}] <= left the chatroom'.encode(
            'utf-8'), server_addr)
        shutdown = True

# recvThread.join()
client.close()
