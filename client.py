import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4500
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main(): 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # Get command from the user
    command = input("Enter command (q for quit, f for file transfer): ")

    # Send command to the server
    client.send(command.encode(FORMAT))

    if command == 'f':
        file = open("data/test.txt", "r")
        data = file.read()

        # Send name of file
        client.send("test.txt".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)

        print(f"SERVER: {msg}")
        
        # Send the data itself
        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)

        print(f"SERVER: {msg}")

        file.close()

    client.close()

if __name__ == "__main__":
    main()