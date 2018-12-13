import sys
import socket
import time

# можно написать так
# socket.gethostbyname(socket.gethostname), где socket.gethostname вернёт имя
# хоста нашей машины, например, ridhost, а полный вызов вернёт ip-адрес
# машины в локальной сети, например 192.168.0.101
# host = socket.gethostbyname('127.0.0.1')
# port = 9090

# Usage: [script] [IP address] [port number]
# or just [script]
if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    # socket.gethostname вернёт имя хоста нашей машины, например, ridhost,
    # а полный вызов вернёт ip-адрес машины в локальной сети, например 192.168.0.101
    host = socket.gethostbyname(socket.gethostname())
    port = 9090

addr = (host, port)

clients = []

# здесь address_family - это IPv4, а протокол транспортного уровня (socket_type) - UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # привязываем сокет к адресу
    s.bind(addr)
except:
    s.close()
    exit()

# по флагу quit производится выход из цикла, в котором сокет слушает соединения
quit = False

print(f'\n[ Server started on {host}:{port} ]\n')

while not quit:
    try:
        # возвращает кортеж (bytes, address), где address зависит от
        # address_family, указанной при создании сокета
        data, addr = s.recvfrom(1024)

        if addr not in clients:
            clients.append(addr)

        client_addr = str(addr[0])
        client_port = int(addr[1])

        itsatime = time.strftime('%Y-%m-%d-%H:%M:%S')

        print(f'[{client_addr}]=[{client_port}]=[{itsatime}]/', end='')
        print(data.decode('utf-8'))

        for client in clients:
            if addr != client:
                s.sendto(data, client)
    except:
        print('\nServer stopped')
        quit = True

s.close()
