import socket
import sys

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
    # Print the prompt and wait for user input
    command = input('ftp> ')

    # Check what command the user has entered
    if command == 'quit':
        # The user wants to quit the program
        break
    elif command.startswith('get '):
        # The user wants to download a file
        filename = command[4:]
        # TODO: Implement file download
    elif command.startswith('put '):
        # The user wants to upload a file
        filename = command[4:]
        # The name of the file
        fileName = filename

        # Open the file
        fileObj = open(fileName, "r")

        # The number of bytes sent
        numSent = 0

        # The file data
        fileData = None

        # Keep sending until all is sent
        while True:
            
            # Read 65536 bytes of data
            fileData = fileObj.read(65536)
            
            # Make sure we did not hit EOF
            if fileData:
                
                    
                # Get the size of the data read
                # and convert it to string
                dataSizeStr = str(len(fileData))
                
                # Prepend 0's to the size string
                # until the size is 10 bytes
                while len(dataSizeStr) < 10:
                    dataSizeStr = "0" + dataSizeStr    
            
                # Prepend the size of the data to the
                # file data.
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
        # The user wants to list the files on the server
        # TODO: Implement file listing
        pass
    else:
        print('Unknown command')

# Close the socket
connSock.close()