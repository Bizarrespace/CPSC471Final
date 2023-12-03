# CPSC471 Final - Python

## Programming Language:
* Python

## Team Members

- **Long Vu**
    - **GitHub:** Bizarrespace
    - **Email:** Longvu2000@csu.fullerton.edu
- **Marcilino Lamiy**
    - **GitHub:** Marcilino421
    - **Email:** Maromicho12@csu.fullerton.edu

- **Kristen Camarena**
    - **GitHub:** kristencamarena
    - **Email:** K.camarena99@csu.fullerton.edu

- **Parish Gutierrez**
    - **GitHub:** ParishGutierrez
    - **Email:** saichandmeda0707@gmail.com

- **Daniel Corona**
    - **GitHub:** DanCorona08
    - **Email:** jimbo497cat@gmail.com

## How to run:

1. Open a terminal and Run the server:
    ```
    python .\serv.py 60000
    ```
2. Open another terminal and Run the client:
    ```
    python .\cli.py localhost 60000
    ```

## Designing the Protocol
**Control Channels**
* Client sends control messages to server to let the server know what action the client wants to take.
* These messages will be strings that start with a command keyword, followed by any parameteres that are needed by that command
* A good example would be "PUT filename"

**Server Responses**
* Responding to each control message with a status message of either OK or error if there was an error

**Message Formats**
* There will be a string of 10 characters at the start of the file sent in order to indicate the size of that file being sent, this allows for additional checks to make sure that both the client sends all the data and the server gets all the data
* All messages will be sent as strings, endline characters will be the sign that the message is done
* This allows for messages to be easy to read using socket.recv and socket.send

**File Transfer Setup**
* Client sends "PUT filename" or "GET filename" message to the server at hand. Server responds with OK if the file exists(for GET) or can be created using our PUT command. Responses with an error message otherwise. 
* Once the client gets the OK message it starts sending or receiving the data

**Start/Stop receiving of files**
* Client knows to start receiving file once it has received OK message from the server, and to indicate that the client is done sending data, it could send a special EOF message after file data.

**Avoiding Buffer overflow**
* Client and server should send and recieve data in small chucks, 1024 bytes for example, ths in ensures sender does not fill buffer faster than the receiver can handle such data.

```
PUT Command:
Client                      Server
------                      ------
PUT filename
                            SUCCESS
<file size>
<file data>


Get command:
Client                      Server
------                      ------
GET filename
                            SUCCESS
<file size>

Ls command:
Client                      Server
------                      ------
LS
                            OK
<file list>

Quit Command:
Client                      Server
------                      ------
QUIT
                            Client Disconnect
```
