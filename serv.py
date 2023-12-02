import socket
import sys
import os

# Command line argument check
if len(sys.argv) < 2:
    print("USAGE: python serv.py <PORT NUMBER>")
    sys.exit(1)

listenPort = int(sys.argv[1])

welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSock.bind(('', listenPort))  # Binds to localhost
welcomeSock.listen(1)

# Directory where to store files from client
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)  # Make sure that the path exists


def recvAll(sock, numBytes):
    recvBuff = b""
    tmpBuff = b""

    # Keep receiving until all is received
    while len(recvBuff) < numBytes:
        # Attempt to receive all bytes
        tmpBuff = sock.recv(numBytes)

        # Check to make sure the other side has not closed
        if not tmpBuff:
            break

        # Add the received bytes to the buffer
        recvBuff += tmpBuff
    return recvBuff


# Accept connections forever
while True:

    print("Waiting for connections...")

    # Accept connections
    clientSock, addr = welcomeSock.accept()

    print("Accepted connection from client: ", addr)
    print("\n")

    command = clientSock.recv(1024).decode()

    if command.startswith('get '):
        # Client wants to download a file
        filename = command[4:]

        filepath = os.path.join(data_dir, filename)

        if os.path.exists(filepath):
            # File exists, send file to the client
            fileSize = os.path.getsize(filepath)
            fileSizeStr = str(fileSize).zfill(10)

            clientSock.send(fileSizeStr.encode())

            with open(filepath, 'rb') as f:
                fileData = f.read()
                clientSock.sendall(fileData)

            print(f"Sent file {filename} to {addr}")

        else:
            # File does not exist
            clientSock.send("FAILURE File does not exist".encode())

    elif command.startswith('put '):
        # Client wants to upload a file
        filename = command[4:]

        fileSizeStr = recvAll(clientSock, 10).decode()
        fileSize = int(fileSizeStr)

        fileData = recvAll(clientSock, fileSize)

        with open(os.path.join(data_dir, filename), 'wb') as f:
            f.write(fileData)

        print(f"Received file {filename} from {addr}")

    elif command == 'ls':
        # Client requests file listing
        file_list = os.listdir(data_dir)
        file_list_str = "\n".join(file_list)
        clientSock.sendall(file_list_str.encode())
        print(f"Sent file list to {addr}")

    else:
        # Unknown command
        print('Unknown command')

    # Close our side
    clientSock.close()
