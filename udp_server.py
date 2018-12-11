import sys
import socket
import time

# можно написать так
# socket.gethostbyname(socket.gethostname), где socket.gethostname вернёт имя
# хоста нашей машины, например, ridhost, а полный вызов вернёт ip-адрес
# машины в локальной сети, например 192.168.0.101
# host = socket.gethostbyname('127.0.0.1')
# port = 9090

if len(sys.argv) != 3:
    print('Usage: script, IP address, port number')
    exit()

host = sys.argv[1]
port = sys.argv[2]

addr = (host, port)

clients = []

# здесь address_family - это IPv4, а протокол транспортного уровня (socket_type) - UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# привязываем сокет к адресу
s.bind(addr)

# по флагу quit производится выход из цикла, в котором сокет слушает соединения
quit = False

print('[ Server started ]')

while not quit:
    try:
        # возвращает кортеж (bytes, address), где address зависит от
        # address_family, указанной при создании сокета
        data, addr = s.recvfrom(1024)

        if addr not in clients:
            clients.append(addr)

        client_addr = str(addr[0])
        client_port = str(addr[1])

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
