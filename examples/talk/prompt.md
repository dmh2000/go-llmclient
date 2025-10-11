in directory @examples/talk, I want to create a new python library file, talk_tcp. this file will encapsulate support for a tcp server and a tcp client. the purpose of this library is to provide a simple interface for creating tcp servers and clients.

- the tcp server function "talk_server", will be given an ip address and a port. it will configure the tcp server to listen on the ip and port. it will return the socket to the caller.
  - it will not perform the accept call in this function.
- there will be 5 funcions:
  - function 'talk_accept' that receives the server socket as a parameter and then performs the accept call. it will wait for a client connection. when the client connects the function will return the client socket. it will only handle a single 'accept' call. no loop.
  - function 'talk_client' that will be given an ip address and port, and will configure a socket as a tcp client then perform the connect and return the socket.
  - there function 'talk*send' that will take a socket and a message as a string, and will send the message to the socket.
    -function 'talk* receive' that will take a socket and will return the message as a string.
  - a function 'talk_close' that will take a socket and will close the socket.

review this specification and let me know if you see any problems. do not create any code until i read your feedback

1. message framing will add a length-prefix protocol with 4 bytes. the talk_send function should add the length prefix to the message and send it.
2. the talk_receive function should read all the data specified by the length prefix, convert it to a string and return it. the receive function should perform multiple reads until it has read all the data specified by the length prefix.
3. the talk_receive function should block until a message is received or the socket is closed by the other end
4. if an error occurs at any point, print an error message and exit the program
5. use UTF-8 encoding
6. the talk_server should perform 'socket', 'bind' and 'listen' calls
7. the listen function in the server should have a backlog of 1

now i want to create a file, examples/talk/bob.py that is similar to alice.py except:

- bob.py will operate as a tcp server
- instead of sending an initial greeting, bob.py will wait for a connection from alice.py
- bob.py receive a message from alice, submit it to query_text and get the response
- bob.py will maintain a context variable. all messages between alice and box in both directions will be added to the context
- the main function will run until the client closes the socket and then exit

review this specification and let me know if you see any problems. do not create any code until i read your feedback. you can use alice.py as a template and then make the changes, however you want to proceed

1. have talk_receive return None if the socket is closed
2. bob system prompt. create a placeholder for the bob system prompt and I will fill it in later.
3. message flow: in a loop, bob will first receive a message from Alice, generate a response and then send it back to Alice. if the client closes the socket, break out of the loop
4. if any errors are detected at any point, print an error message and exit the program
5. after the client disconnects, exit the program. the bob server will only handle a single connection

I want to create a web app as follows:

1. intitialize a vanilla vite app with typescript. the app will be located in the directory examples/talk/alice
2. the front end will show the name 'Alice'. it will open a websocket connection to the backend. the backend will occasionally send the url of an mp3 file on the websocket connection. the front end will play the mp3 file when it receives it from the backend.
3. the backend will use the node f.watch function for a specific file name and when the file is created or changed it will send the url of the mp3 file to the front end via the websocket connection. the mp3 file will be in the same directory as the index.html file.

I want to create another web app as follows:

1. intitialize a vanilla vite app with typescript. the app will be located in the directory examples/talk/bob.
2. the front end will show the name 'Bob. it will open a websocket connection to the backend.
3. this app is almost identical to the alice app, except that when it starts, instead of a start button, it will show the name 'Bob' and a text box and a submit button. when the user enters text in the text box and submits it, the text will be sent to the backend via the websocket connection. the backend will send a response. create a placeholder function for the text response from the websocket. I will fill it in later.
4. the backend will occasionally send the url of an mp3 file on the websocket connection. the front end will play the mp3 file when it receives it from the backend.
5. the backend will use the node f.watch function for a specific file name and when the file is created or changed it will send the url of the mp3 file to the front end via the websocket connection. the mp3 file will be in the same directory as the index.html file.
