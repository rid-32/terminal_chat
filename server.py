import socket
import sys
import time
from threading import Thread

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

# создаём сокет с address_family IPv4 и socket_type - TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # привязываем сокет к адресу
    server.bind(addr)
except:
    print(f'\n[ Address {host}:{port} can`t be bind to the socket ]\n')

    server.close()

    exit()

# говорим сокету слушать входящие соединения. 100 - число входящих соединений в
# очереди. Если одновременных соединений больше 100, то лишние отбрасываются
server.listen(100)

# список подключенных к chat_room клиентов. в нём хранятся соединения
clients = []
names = []

print(f'\n[ Server started on {host}:{port} ]\n')


class ClientThread(Thread):
    '''класс создания потока соединения с клиентом'''

    def __init__(self, address, connection):
        '''сохраняем соединение'''
        Thread.__init__(self)

        self.connection = connection
        self.address = address

    def run(self):
        '''функция run запускается после вызова метода start() на созданном потоке'''

        client_addr = str(self.address[0])
        client_port = str(self.address[1])

        # сначала получаем от пользователя имя
        name = self.connection.recv(2048)
        name = name.decode('utf-8')

        # отправляем пользователю приветственное сообщение
        self.connection.send(
            'Welcome to a chatroom'.encode('utf-8'))

        # добавляем имя пользователя в пулл имён
        if name not in names:
            names.append(name)

        # сообщим всем пользователям этой chat_room, что присоединился новый участник
        welcomeMessage = f'[ {name} ] joined to the chatroom'
        broadcast(welcomeMessage.encode('utf-8'), conn)

        # флаг закрытия потока (завершения функции run)
        closeTread = False

        while not closeTread:
            try:
                # при первой же итерации выполнение потока останавливается здесь
                # ждём получение данных от self.connection
                # если пришло пустое сообщение, значит клиент разорвал соединение
                message = self.connection.recv(2048)
                message = message.decode('utf-8')

                if message:
                    answer = f'[ {name} ]: {message}'
                    print(answer)

                    broadcast(answer.encode('utf-8'), self.connection)
                else:
                    # логгируем дату и время отключения нового клиента
                    itsatime = time.strftime('%Y-%m-%d-%H:%M:%S')

                    print(
                        f'[{client_addr}]=[{client_port}]=[{itsatime}] => left the chatroom')

                    # сообщаем всем пользователям, что участник покинул чат
                    # удаляем соединение из пула и закрываем поток,
                    # т.е. просто выходим из цикла, чтобы ф-ция run завершилась
                    byeMessage = f'[ {name} ] left the chatroom'

                    broadcast(byeMessage.encode('utf-8'), self.connection)
                    remove(self.connection)

                    closeTread = True
            except:
                # я хз, зачем это тут)
                continue


def broadcast(message, connection):
    '''функция отправки сообщения message всем клиентам в списке clients'''
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)


def remove(connection):
    '''функция удаления соединения из списка clients'''
    if connection in clients:
        clients.remove(connection)


quit = False

while not quit:
    try:
        # при первой же итерации выполнение программы остановится здесь,
        # пока не будет получено новое соединение
        conn, addr = server.accept()

        # добавляем новое соединение в пулл соединений
        if conn not in clients:
            clients.append(conn)

        client_addr = str(addr[0])
        client_port = str(addr[1])

        itsatime = time.strftime('%Y-%m-%d-%H:%M:%S')

        # логгируем дату и время подключения нового клиента
        print(
            f'[{client_addr}]=[{client_port}]=[{itsatime}] <= joined to the chatroom')

        # создаём новый поток, передаём ему новое соединение и запускаем поток
        client_thread = ClientThread(addr, conn)
        client_thread.start()
    except:
        # TODO ПОЛУЧИТЬ ВСЕ ПОТОКИ И ЗАКРЫТЬ ИХ
        print('\nServer stopped')
        quit = True

server.close()
