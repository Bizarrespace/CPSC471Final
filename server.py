import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4500
ADDR = (IP, PORT)

def main(): 
    print("STARTING SERVER")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET for IPV4, SOCK_STREAM for TCP connection type
    server.bind(ADDR)
    server.listen()
    print("LISTENING FOR CONNECTION")

    while True:
        connection, address = server.accept()
        print(f"NEW CONNECTION {address} CONNECTED")

if __name__ == "__main__":
    main()