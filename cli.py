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

# Create a TCP socket for control connection
control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
control_sock.connect((server_addr, server_port))

# Create a TCP socket for data connection
data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_sock.bind(('localhost', 0))  # Bind to an ephemeral port
data_port = data_sock.getsockname()[1]

# Tell the server our data port
control_sock.send(f'DATA_PORT {data_port}'.encode())

# Wait for the server to connect to our data port
data_sock.listen(1)
data_conn, _ = data_sock.accept()

while True:
    command = input('ftp> ')

    # Check what command the user has entered
    if command == 'quit':
        break
    elif command.startswith('get '):
        # The user wants to download a file
        file_name = command[4:]
        # this is to receive file size and data
        control_sock.send(command.encode())
        file_size_str = control_sock.recv(10).decode()

        if file_size_str.startswith("FAILURE"):
            print("File does not exist!")
            continue

        file_size = int(file_size_str)
        file_data = data_conn.recv(file_size)

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
        control_sock.sendall(command.encode())
        file_size = os.path.getsize(file_path)
        file_size_str = pad_zeros(file_size, 10)
        control_sock.send(file_size_str.encode())

        with open(file_path, 'rb') as f:
            file_data = f.read()
            data_conn.sendall(file_data)

        print(f"Sent file {file_name} of size {file_size} bytes")

    elif command == 'ls':
        # The user wants to list the files on the server
        # This is to receive and print the file list for the ls command
        control_sock.sendall(command.encode())
        file_list = data_conn.recv(4096).decode()
        print(file_list)
    else:
        print('Unknown command')

# Close the sockets
control_sock.close()
data_conn.close()