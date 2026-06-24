# Multi-Room Chat Application
# Contributors- Samuel Kisilu Musau - GH104598 - Server Implementation, room management, private messaging- 
		Leon Kimutai Langat - GH1046169 - Client Implementation, testing, documentation.


## Overview

This is a real-time chat application built using Python's socket programming library. It follows a client-server architecture and supports multiple users, group chat rooms, and private messaging. The application was developed as a group project for the B205 Computer Networks course at Gisma University of Applied Sciences.

## Features

- Multiple users can connect simultaneously
- Create new chat rooms
- Switch between existing chat rooms
- Invite other users to your current room
- Private messaging between users
- Unique nickname validation (duplicate names are rejected)
- Real-time message broadcasting to rooms
- Console-based user interface
- Error handling and logging on the server

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| /create <room_name> | Creates a new room and joins it | /create Gaming |
| /join <room_name> | Switches to an existing room | /join Lobby |
| /list | Shows all rooms and their members | /list |
| /invite <nickname> | Invites a user to your current room | /invite Alice |
| /msg <nickname> <message> | Sends a private message to a user | /msg Bob Hello! |
| Any other text | Sends a chat message to your current room | Hello everyone! |

## Installation

### Prerequisites
- Python 3.6 or higher installed on your system
- All devices must be on the same local network

### Server Setup (Windows)
1. Open Command Prompt
2. Navigate to the project folder: cd C:\Users\YourUsername\Desktop\Computer Networks Chat Program
3. Start the server: python f_server.py
4. Note the server's IP address displayed in the console

### Client Setup (Windows/macOS/Linux)
1. Open Terminal or Command Prompt
2. Navigate to the project folder
3. Start the client: python f_client.py
4. Enter a unique nickname when prompted

## Usage Guide

### Starting the Server
1. Run the server script first
2. The server will display: "Server is listening for connections..."
3. Keep this window open throughout the chat session

### Starting Clients
1. Each user runs the client script on their device
2. Enter a unique nickname (no two users can have the same name)
3. You are automatically placed in the default "Lobby" room
4. Type /list to see available rooms and who is in them

### Creating and Joining Rooms
- To create a room: /create RoomName
- To switch rooms: /join RoomName
- To see all rooms: /list

### Inviting Users
- To invite someone to your current room: /invite Nickname
- The invited user will receive a private message with instructions

### Private Messaging
- To send a private message: /msg Nickname Your message here
- Only the sender and recipient see the message

## System Architecture

The application uses a Client-Server architecture:

- Server: A central Windows machine running the server script. It manages all connections, rooms, and message routing.
- Clients: Any device (Windows, macOS, Linux) running the client script. Users connect to the server via TCP.

### Communication Protocol

The application uses TCP (Transmission Control Protocol) with the following characteristics:

- Transport Protocol: TCP on port 55555
- Encoding: ASCII text encoding
- Message Format: Plain text strings
- Handshake: Server sends "NICK" to request username, client replies with chosen name
- Command Format: Commands start with "/" (e.g., /create Gaming)

### Why TCP?

TCP was chosen because:
- Reliable delivery - messages always arrive
- Ordered delivery - messages arrive in the correct sequence
- Error recovery - built-in retransmission for lost packets
- Stream-oriented - suitable for text-based communication

### Protocol Analysis

| Protocol | Pros | Cons |
|----------|------|------|
| TCP | Reliable, ordered delivery, error recovery | Slightly higher latency, stateful |
| UDP | Faster, low latency | Unreliable, out-of-order delivery |

For a chat application, reliability and message ordering are essential. TCP ensures that messages arrive in the correct sequence and are not lost. UDP would be inappropriate because messages could be dropped or arrive out of order, disrupting the conversation flow.

## File Structure
Computer Networks Chat Program/
├── f_server.py # Server application
├── f_client.py # Client application
└── README.md # This file

## Error Handling

The application includes error handling for:
- Duplicate nicknames (users are rejected and disconnected)
- Network disconnections (clients are removed from all rooms)
- Invalid commands (users receive usage instructions)
- Failed message delivery (errors are logged on the server)

## Configuration

To change the server IP address, edit the following line in both files:

**f_server.py:**
```python
host = '192.168.2.34'  # Replace with your current IP
client.connect(('192.168.2.34', 55555))  # Replace with server IP





