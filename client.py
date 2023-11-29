import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4500
ADDR = (IP, PORT)

def main(): 
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET for IPV4, SOCK_STREAM for TCP connection type
    client.connect(ADDR)
    
    
if __name__ == "__main__":
    main()