import socket
import gpiozero  # The GPIO library for Raspberry Pi
import time  # Enables Python to manage timing

# define the rpi GPIO
led = gpiozero.LED(26) # Reference GPIO26

# Define server address and port
host = '0.0.0.0'  # Listen on all available interfaces
port = 80

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections (max queued connections is 5)
server_socket.listen(5)
print(f"Server listening on {host}:{port}")


while True:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    led.on() # Turn LED on

    # Send a welcome message to the client
    welcome_message = "Welcome to the chat server! Type 'bye' to exit.!!!!!"
    client_socket.send(welcome_message.encode())

    print(f"Type a message to start a conversation with {client_address}")

    # Send message to the client
    response_message = input("Your message: ")
    client_socket.send(response_message.encode())

    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        #led.on() # Turn LED on
        if not data:
            break

        # Convert bytes to string
        received_message = data.decode()

        # Print the received message
        print(f"Received message from {client_address}: {received_message}")

        # Check if the client wants to exit
        if received_message.lower() == 'bye':
            break

        # Get a response from the server user
        response_message = input("Your response: ")

        # Send the response back to the client
        client_socket.send(response_message.encode())



    print(f"Connection with {client_address} closed.")
    client_socket.close()
    led.off() # Turn LED off

    




'''
while True:
  
  time.sleep(1)
  led.off() # Turn the LED off
  time.sleep(1)  # Pause for 1 second
'''