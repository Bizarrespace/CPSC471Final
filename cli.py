import socket
import sys


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
        # 
        #
        # TODO: Implement file download
        #
        #
    elif command.startswith('put '):
        # The user wants to upload a file
        fileName = command[4:]

        #Send filename
        connSock.sendall(fileName.encode())
        # Open the file
        fileObj = open(fileName, "r")

        # The number of bytes sent
        numSent = 0

        # The file data
        fileData = None

        # Keep sending until all is sent
        while True:
            fileData = fileObj.read(65536)

            # Make sure we did not hit EOF
            if fileData:
                # Get the size of the data
                dataSize = len(fileData)
                dataSizeStr =  padZeros(dataSize, 10)
            
                fileData = dataSizeStr + fileData    
                
                # The number of bytes sent
                numSent = 0

                # Send the data!
                while len(fileData) > numSent:
                    numSent += connSock.send(fileData[numSent:].encode())

            # The file has been read. We are done
            else:
                break

        print ("Sent ", numSent, " bytes.")

        # Close the file
        fileObj.close()
    elif command == 'ls':
        #
        #
        # The user wants to list the files on the server
        # TODO: Implement file listing
        #
        pass
    else:
        print('Unknown command')

# Close the socket
connSock.close()