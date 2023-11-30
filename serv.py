import socket
import sys 
import os

# Command line arugment check
if len(sys.argv) < 2:
    print("USAGE: python serv.py <PORT NUMBER>")
    sys.exit(1)

listenPort = int(sys.argv[1])

welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSock.bind(('', listenPort)) #Binds to localhost
welcomeSock.listen(1)

# Directory where to store files from client
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True) # Make sure that the path exists


def recvAll(sock, numBytes):
    recvBuff = b""
    tmpBuff = b""

    # Keep receiving till all is received
    while len(recvBuff) < numBytes:
        # Attempt to receive all bytes
        tmpBuff =  sock.recv(numBytes)

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

    filename = clientSock.recv(1024).decode()
    fileData = ""

    # The temporary buffer to store the received data
    recvBuff = ""
    fileSizeBuff = ""
    
    fileSize = 0	

    # Receive the first 10 bytes indicating the
    # size of the file
    fileSizeBuff = recvAll(clientSock, 10)
        
    fileSize = int(fileSizeBuff)

    print("The file size is", fileSize)

    # Get the file data
    fileData = recvAll(clientSock, fileSize)

    # Write the data to a file in the data directory
    with open(os.path.join(data_dir, filename), 'wb') as f:
        f.write(fileData)

    print(f"Received file {filename}")

    # Close our side
    clientSock.close()