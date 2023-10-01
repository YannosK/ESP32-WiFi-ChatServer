import socket
import select
import gpiozero
import threading

# Define the rpi GPIO
led = gpiozero.LED(26)  # Reference GPIO26

# Define a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Function to initialize the server
def init():
    # Define server address and port
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 80

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections (max queued connections is 5)
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")


# Function to handle client communication
def handle_client(client_socket):
    # Send a welcome message to the client
    welcome_message = "Welcome to the chat server! Type 'bye' to exit."
    client_socket.send(welcome_message.encode())

    while True:
        try:
            # Check if there is data available for reading from the client socket
            readable, _, _ = select.select([client_socket], [], [], 0.1)

            if readable:
                # Receive data from the client
                data = client_socket.recv(1024)

                if not data:
                    print(f"Connection with {client_address} closed.")
                    client_socket.close()
                    led.off()  # Turn LED off
                    break

                # Convert bytes to string
                received_message = data.decode()

                # Print the received message
                print(f"Received message from {client_address}: {received_message}")

                # Check if the client wants to exit
                if received_message.lower() == 'bye':
                    print(f"Connection with {client_address} closed.")
                    client_socket.close()
                    led.off()  # Turn LED off
                    break
            else:
                pass

        except socket.error:
            # Handle socket errors (e.g., client disconnects)
            print(f"Connection with {client_address} closed.")
            client_socket.close()
            led.off()  # Turn LED off
            break

# Function to handle input from server
def server_input():
    while True:
        response_message = input("Your response: ")

        # Send the response to all connected clients
        for client_socket in clients:
            client_socket.send(response_message.encode())

# Initialize the server
init()

# Create a list to store client sockets
clients = []

# Start the server input thread
input_thread = threading.Thread(target=server_input)
input_thread.start()

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    led.on()  # Turn LED on

    # Add the client socket to the list
    clients.append(client_socket)

    # Start a new thread to handle client communication
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
