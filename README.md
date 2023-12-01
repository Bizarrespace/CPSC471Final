# CPSC471 Final

## Members

* Long Vu -- Longvu2000@csu.fullerton.edu
* Marcilino Lamiy -- Maromicho12@csu.fullerton.edu
* Kristen Camarena --
* Parish Gutierrez -- 
* Daniel Corona --  

## Getting Started

* To Run 
* python .\serv.py 60000
* python .\cli.py localhost 60000

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
Client                      Server
------                      ------
PUT filename
                            OK
<file data>
EOF
                            OK


Client                      Server
------                      ------
GET filename
                            OK
                            <file data>
                            EOF
OK       
```