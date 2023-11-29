import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4500
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main(): 
    print("STARTING SERVER")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("LISTENING FOR CONNECTION")

    running = True
    while running:
        connection, address = server.accept()
        print(f"NEW CONNECTION {address} CONNECTED")

        # Get command from the client
        command = connection.recv(SIZE).decode(FORMAT)

        if command == 'q':
            print(f"CLIENT {address} disconnected")
            connection.close()
            running = False
        elif command == 'f':
            # Get file name from the client
            filename = connection.recv(SIZE).decode(FORMAT)
            print("RECEIVED File")

            file = open(filename, "w")
            connection.send("Filename Received". encode(FORMAT))

            # Get file data from the client
            data = connection.recv(SIZE).decode(FORMAT)
            print("File data received")

            # Write data into the file and send confirmation
            file.write(data)
            connection.send("File data Received".encode(FORMAT))

            file.close()
            connection.close()
            print(f"CLIENT {address} disconnected")

    print("SERVER SHUTTING DOWN")
    server.close()    
if __name__ == "__main__":
    main()