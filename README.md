# StudyChat
A-Level Non examined coursework. This is the combination of the networking files and the GUI files.

To run the application:
- Run the __init__ file in the server folder (this will start a socket listening on port 5055)
- Run the __init__ file in the client folder (this will connect to the server socket and a GUI will be created) 


To send commands: 
- Use the .send_command method in either the client_socket or server_socket classes with the command name and arguments provided.
If the size of the command is too large it will be droped and if the command name is invalid, or any of the arguments cannot be matched, then the command will also be ignored on the receiving side


Issues:
- Depending on the network you are connected to, the port for the TIE server for the smpt lib library may be blocked. This results in the server program breaking and no connections can be made.
- Run time error:  can't create new thread at interpreter shutdown. This issue occours only on mac and to tempoary fix this downgrade to a version lower than 3.12
