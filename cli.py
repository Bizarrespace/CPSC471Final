import socket
import sys
import os


def padZeros(number, length):
    """Return string representation of number padded with 0s"""
    number_str = str(number)
    while len(number_str) < length:
        number_str = "0" + number_str
    print(number_str)
    return number_str

# Command line checks 
if len(sys.argv) < 3:
    print("USAGE: python cli.py <SERVER MACHINE> <SERVER PORT>")
    sys.exit(1)

# Get info from the command line
serverMachine = sys.argv[1]
serverPort = int(sys.argv[2])

# Convert name to IP address
serverAddr = socket.gethostbyname(serverMachine)

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

while True:
    command = input('ftp> ')

    # Check what command the user has entered
    if command == 'quit':
        break
    elif command.startswith('get '):
        # The user wants to download a file
        fileName = command[4:]
        # TODO: Implement file download
        # this is to recieve file size and data
        connSock.send(command.encode())
        fileSizeStr = connSock.recv(10).decode()
        fileSize = int(fileSizeStr)
        fileData = connSock.recv(fileSize)

        with open(fileName, 'wb') as f:
            f.write(fileData)

        print(f"Received file {fileName}")
        
    elif command.startswith('put '):
        # This is to upload a file, ge file size and send the file data
        fileName = command[4:]
        connSock.sendall(command.encode())
        fileSize = os.path.getsize(fileName)
        fileSizeStr = padZeros(fileSize, 10)
        connSock.send(fileSizeStr.encode())

        with open(fileName, 'rb') as f:
            fileData = f.read()
            connSock.sendall(fileData)

        print(f"Sent file {fileName}")
        
    elif command == 'ls':
        # The user wants to list the files on the server
        # TODO: Implement file listing
        # This is to receive and print the file list for the ls command
        connSock.sendall(command.encode())
        file_list = connSock.recv(4096).decode()
        print(file_list)
        pass
    else:
        print('Unknown command')

# Close the socket
connSock.close()