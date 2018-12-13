import sys
import socket
import select

if len(sys.argv) != 3:
    print('Usage: [script] [server IP adress] [server port number]')
    exit()

try:
    name = str(input('Name: '))
except:
    print('\n[ Goodbye ]')
    exit()

host = str(sys.argv[1])
port = int(sys.argv[2])

addr = (host, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # подключаемся к серверу
    server.connect(addr)
    # отправляем серверу имя пользователя
    server.send(name.encode('utf-8'))
except:
    print('\n[ Connection couldn`t be established ]\n')
    exit()

quit = False

while not quit:
    try:
        sockets = [sys.stdin, server]

        # при первой же итерации выполнение программы остановится здесь
        # пока не произойдёт чтение либо из stdin, либо из сокета
        read_sockets, write_sockets, error_socket = select.select(
            sockets, [], [])

        for read_socket in read_sockets:
            if read_socket == server:
                message = read_socket.recv(2048)
                print(f"\n{message.decode('utf-8')}")
            else:
                message = str(input('> '))

                if message != '':
                    server.send(message.encode('utf-8'))
    except:
        print('\nGoodbye')
        quit = True

server.close()
