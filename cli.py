import socket
import sys
import os


def pad_zeros(number, length):
    """Return string representation of number padded with 0s"""
    number_str = str(number)
    while len(number_str) < length:
        number_str = "0" + number_str
    return number_str


# Command line checks
if len(sys.argv) < 3:
    print("USAGE: python cli.py <SERVER MACHINE> <SERVER PORT>")
    sys.exit(1)

# Get info from the command line
server_machine = sys.argv[1]
server_port = int(sys.argv[2])

# Convert name to IP address
server_addr = socket.gethostbyname(server_machine)

# Create a TCP socket
conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
conn_sock.connect((server_addr, server_port))

while True:
    command = input('ftp> ')

    # Check what command the user has entered
    if command == 'quit':
        break
    elif command.startswith('get '):
        # The user wants to download a file
        file_name = command[4:]
        # this is to receive file size and data
        conn_sock.send(command.encode())
        file_size_str = conn_sock.recv(10).decode()

        if file_size_str.startswith("FAILURE"):
            print("File does not exist!")
            continue
    
        file_size = int(file_size_str)
        file_data = conn_sock.recv(file_size)

        os.makedirs('clientData', exist_ok=True)


        with open(os.path.join('clientData', file_name), 'wb') as f:
            f.write(file_data)

        print(f"Received file {file_name} of size {file_size} bytes")
        
    elif command.startswith('put '):
        # This is to upload a file, get file size and send the file data
        file_name = command[4:]
        file_path = os.path.join('clientData', file_name)
        if not os.path.exists(file_path):
            print("FAILURE: File does not exist")
            continue
        conn_sock.sendall(command.encode())
        file_size = os.path.getsize(file_path)
        file_size_str = pad_zeros(file_size, 10)
        conn_sock.send(file_size_str.encode())

        with open(file_path, 'rb') as f:
            file_data = f.read()
            conn_sock.sendall(file_data)

        print(f"Sent file {file_name} of size {file_size} bytes")
        
    elif command == 'ls':
        # The user wants to list the files on the server
        # TODO: Implement file listing
        # This is to receive and print the file list for the ls command
        conn_sock.sendall(command.encode())
        file_list = conn_sock.recv(4096).decode()
        print(file_list)
        pass
    else:
        print('Unknown command')

# Close the socket
conn_sock.close()
