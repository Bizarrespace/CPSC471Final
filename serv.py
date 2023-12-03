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
data_dir = 'serverData'
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
try:

    while True:

        print("Waiting for connections...")

        # Accept connections
        control_sock, addr = welcomeSock.accept()

        # Get the data port from the client
        data_port_msg = control_sock.recv(1024).decode()
        data_port = int(data_port_msg.split()[1])

        # Create a TCP socket for data connection
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.connect((addr[0], data_port))  # Connect to the client's data port

        print("Accepted connection from client: ", addr)
        print("\n")

        while True:
            try:
                command = control_sock.recv(1024).decode()

                # Catches when the client disconnects
                if not command:
                    print("Client has disconnected")
                    break

                if command.startswith('get '):
                    # Client wants to download a file
                    filename = command[4:]

                    filepath = os.path.join(data_dir, filename)

                    if os.path.exists(filepath):
                        # File exists, send file to the client
                        fileSize = os.path.getsize(filepath)
                        fileSizeStr = str(fileSize).zfill(10)

                        control_sock.send(fileSizeStr.encode())

                        with open(filepath, 'rb') as f:
                            fileData = f.read()
                            data_sock.sendall(fileData)

                        print(f"SUCCESS: Sent file {filename} to {addr}")

                    else:
                        # File does not exist
                        control_sock.send("FAILURE File does not exist".encode())
                        print(f"FAILURE: File {filename} does not exist")

                elif command.startswith('put '):
                    # Client wants to upload a file
                    filename = command[4:]

                    fileSizeStr = recvAll(control_sock, 10).decode()
                    fileSize = int(fileSizeStr)

                    fileData = recvAll(data_sock, fileSize)

                    with open(os.path.join(data_dir, filename), 'wb') as f:
                        f.write(fileData)

                    print(f"SUCCESS: Received file {filename} from {addr}")

                elif command == 'ls':
                    # Client requests file listing
                    file_list = os.listdir(data_dir)
                    file_list_str = "\n".join(file_list)
                    data_sock.sendall(file_list_str.encode())
                    print(f"SUCCESS: Sent file list to {addr}")

                else:
                    # Unknown command
                    print('Unknown command')
            except ConnectionAbortedError:
                print("Client has disconnected")
                break
            except KeyboardInterrupt:
                print("Server is shutting down...")
                welcomeSock.close()
                sys.exit(0)

        # Close our side
        control_sock.close()
        data_sock.close()

except KeyboardInterrupt:
    print("Server is shutting down...")
    welcomeSock.close()
    sys.exit(0)