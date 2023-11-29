import socket

serverPort = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(('localhost', serverPort))

serverSocket.listen(1)

print("The server is ready to receive")

data = ""

while True:
    connectionSocket, addr = serverSocket.accept()

    data = connectionSocket.recv(40)

    print(data)

    connectionSocket.close()

