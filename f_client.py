import socket
import threading

nickname = input("Choose a nickname: ") # Receive nickname input from user and store it in the variable

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Change IP Address to hosts' current IP
client.connect(('192.168.2.34', 55555))

# Function for receiving messages
def receive(): 
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                # Server is asking for nickname
                client.send(nickname.encode('ascii'))
            elif message == 'DUPLICATE':
                print("[SERVER]: Nickname already taken! Closing...")
                client.close()
                break
            else:
                # Print any normal message from the server/chat
                print(message)
        except:
            print("Disconnected from server.")
            client.close()
            break

# Function for writing messages
def write():
    while True:
        message = input("")
        if message:
            client.send(message.encode('ascii'))

# Start threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()