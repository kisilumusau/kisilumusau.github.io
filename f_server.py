#################### WIR MUSSEN ZUERST DIE IP-ADDRESSEN ANDERN ######################

import threading
import socket

# --- Server Config ---

host = '192.168.2.34' # Your current IP
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
server.bind((host, port)) # Bind the socket to the host and port
server.listen() # Start listening for incoming connections

# --- Data Structures --- 

# Lists to keep track of clients and their nicknames
clients = [] 
nicknames = []

# Dictionary to keep track of which room each client is in
client_rooms = {}
rooms = {}

# Define default room
DEFAULT_ROOM = "Lobby"
rooms[DEFAULT_ROOM] = []

# Helper functions
def find_client_by_nickname(nickname):
    for idx, nick in enumerate(nicknames): # Loop through nicknames to find the client
        if nick == nickname: #  If the nickname matches, return the corresponding client
            return clients[idx]
    return None

def broadcast_to_room(message, room_name, skip_client=None):
    if room_name in rooms:
        for client in rooms[room_name]:
            if client != skip_client:
                try:
                    client.send(message)
                except:
                    print(f"Error occurred while sending message to client: {client}") # Error handling if sending fails
                    pass

def send_private(client, message):
    try:
        client.send(f"[SERVER]: {message}".encode('ascii'))  
    except:
        print(f"Error occurred while sending private message to client: {client}") # Error handling if sending fails
        pass

# Handle client messages
def handle(client):
    while True: # Keep the connection open to receive messages from the client (Infinite loop)
        try:
            message = client.recv(1024).decode('ascii')
            if not message:
                break

            # Command handling
            if message.startswith('/'):
                parts = message.split(' ', 1) # Split the message into command and argument
                cmd = parts[0].lower() # Get the command 
                arg = parts[1] if len(parts) > 1 else "" # Get the argument if it exists

                current_room = client_rooms.get(client, DEFAULT_ROOM) # Get the current room of the client # Default to DEFAULT_ROOM if not found
                sender_nick = nicknames[clients.index(client)] # Get the nickname of the sender

                if cmd == '/create': # Create a new room
                    if not arg: # If no room name is provided, send usage message
                        send_private(client, "Usage: /create <room_name>")
                    elif arg in rooms: # If the room already exists, send an error message
                        send_private(client, f"Room '{arg}' already exists!")
                    else: # Create the new room and move the client to it
                        rooms[arg] = []
                        if current_room in rooms and client in rooms[current_room]:
                            rooms[current_room].remove(client)
                        rooms[arg].append(client)
                        client_rooms[client] = arg
                        send_private(client, f"Room '{arg}' created and you joined it!")
                        broadcast_to_room(f"[SYSTEM]: {sender_nick} created and joined room '{arg}'".encode('ascii'), arg)

                elif cmd == '/msg': # User to User private messaging
                    if not arg:
                        send_private(client, "Usage: /msg <nickname> <message>")
                    else: # Split into target nickname and the message
                        parts_msg = arg.split(' ', 1)
                        if len(parts_msg) < 2:
                            send_private(client, "Usage: /msg <nickname> <message>")
                        else:
                            target_nick = parts_msg [0]
                            private_message = parts_msg [1]

                            # Find the target client
                            target_client = find_client_by_nickname(target_nick)
                            if not target_client:
                                send_private(client, f"User '{target_nick}' not found or offline.")
                            else: # Send the private message to the target
                                send_private(target_client, f"[PRIVATE from {sender_nick}]: {private_message}")
                                send_private(client, f"[PRIVATE to {target_nick}]: {private_message}") #Server log
                                
                elif cmd == '/join': # Join an existing room
                    if not arg: # If no room name is provided, send usage message
                        send_private(client, "Usage: /join <room_name>")
                    elif arg not in rooms: # If the room doesn't exist, send an error message
                        send_private(client, f"Room '{arg}' doesn't exist! Use /list to see rooms.")
                    else: # Move the client to the specified room
                        if current_room in rooms and client in rooms[current_room]:
                            rooms[current_room].remove(client)
                        rooms[arg].append(client)
                        client_rooms[client] = arg
                        send_private(client, f"Switched to room '{arg}'")
                        broadcast_to_room(f"[SYSTEM]: {sender_nick} joined the room".encode('ascii'), arg)

                elif cmd == '/list': # List all available rooms
                    room_list = "Available rooms:\n" # Start the room list with a header
                    for room_name, members in rooms.items(): # Loop through each room and its members
                        member_names = [] # Get the nicknames of the members in the room
                        for c in members: # Loop through each client in the room
                            if c in clients: # Check if the client is still connected
                                idx = clients.index(c) # Get the index of the client in the clients list
                                member_names.append(nicknames[idx]) # Append the nickname of the client to the member_names list
                        room_list += f" - {room_name} ({len(members)} users): {', '.join(member_names)}\n" # Add the room name, number of users, and their nicknames to the room list
                    send_private(client, room_list)

                elif cmd == '/invite': # Invite a user to the current room
                    if not arg: # If no nickname is provided, send usage message
                        send_private(client, "Usage: /invite <nickname>")
                    else: # Find the target client by nickname and send an invite message
                        target_client = find_client_by_nickname(arg) 
                        if not target_client: # If the target client is not found, send an error message
                            send_private(client, f"User '{arg}' not found!")
                        else: # If the target client is found, send an invite message to them and notify the sender
                            room_name = client_rooms.get(client, DEFAULT_ROOM) # Get the current room of the sender
                            send_private(target_client, f"*** {sender_nick} invited you to room '{room_name}'! Type /join {room_name} to join. ***") # Send the invite message to the target client
                            send_private(client, f"Invite sent to {arg}.") # Notify the sender that the invite was sent

                else: # Handle unknown commands
                    send_private(client, f"Unknown command: {cmd}. Commands: /create, /join, /list, /invite") # Send a message to the client indicating that the command is unknown and provide a list of available commands

            else:
                # Normal chat message
                current_room = client_rooms.get(client, DEFAULT_ROOM) # Get the current room of the client # Default to DEFAULT_ROOM if not found
                sender_nick = nicknames[clients.index(client)] # Get the nickname of the sender
                full_msg = f"{sender_nick}: {message}".encode('ascii') # Add the sender's nickname to the message # Encode the message to bytes before broadcasting
                broadcast_to_room(full_msg, current_room, skip_client=client) # Broadcast the message to all clients in the current room, except the sender

        except:
            print(f"Error occurred while handling message from client: {client}") # Error handling if receiving fails
            break

 # Disconnect
def new_func(client):
    if client in clients: # Check if the client is still in the clients list before attempting to remove them
        idx = clients.index(client) # Get the index of the client in the clients list
        nickname = nicknames[idx] 
        for room in rooms.values(): # Loop through all rooms to remove the client from any room they may be in
            if client in room: # Remove the client from the room if they are in it
                room.remove(client) 
        clients.remove(client) # Remove the client from the clients list
        nicknames.remove(nickname) # Remove the nickname from the nicknames list
        client.close() # Close the client's socket connection
        broadcast_to_room(f"[SYSTEM]: {nickname} left the chat.".encode('ascii'), DEFAULT_ROOM)
        print(f"{nickname} disconnected.")

# Accept new connections
def receive(): # Keep the server running to accept new connections
    while True: 
        client, address = server.accept() # Accept a new connection from a client
        print(f"Connected with {str(address)}") # Print the address of the connected client

        client.send('NICK'.encode('ascii')) # Send a request to the client for their nickname
        nickname = client.recv(1024).decode('ascii') # Receive their nickname and set it to the variable

        if nickname in nicknames: # Handle duplicity and maintain originality of nicknames
            client.send('DUPLICATE'.encode('ascii'))
            client.close() # Close the client's socket connection
            continue

        nicknames.append(nickname) # Add their nickname to the variable list
        clients.append(client) # Add the client to the client list
        client_rooms[client] = DEFAULT_ROOM # Send them to the default room
        rooms[DEFAULT_ROOM].append(client) # Add their presence to the default room list
        print(f"Nickname: {nickname}") # Print nickname for server logs
        broadcast_to_room(f"[SYSTEM]: {nickname} joined the chat!".encode('ascii'), DEFAULT_ROOM) # Broadcast their presence to the room
        send_private(client, f"Welcome {nickname}! Type /list to see rooms, /create to make one, /join to switch, /invite to invite.") # Welcome the client privately

        thread = threading.Thread(target=handle, args=(client,)) # Hanle simultaneous messages and multiple user connections
        thread.start() 

print("Server is listening for connections...") # Display message to console
receive() # Call receive function
