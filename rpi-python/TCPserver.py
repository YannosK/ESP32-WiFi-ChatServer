import socket
import select
import gpiozero  # The GPIO library for Raspberry Pi

 # define the rpi GPIO
led = gpiozero.LED(26) # Reference GPIO26

# define a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def init():
    # Define server address and port
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 80

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections (max queued connections is 5)
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

def loop():
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    led.on() # Turn LED on
    
     # Send a welcome message to the client
    welcome_message = "Welcome to the chat server! Type 'bye' to exit.!"
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
                    break

                # Convert bytes to string
                received_message = data.decode()

                # Print the received message
                print(f"Received message from {client_address}: {received_message}")

                # Check if the client wants to exit
                if received_message.lower() == 'bye':
                    print(f"Connection with {client_address} closed.")
                    break
            else:            
                print(f"Type a message to start a conversation with {client_address}")
                # Get a response from the server user
                response_message = input("Your response: ")

            # Send the response back to the client
            client_socket.send(response_message.encode())

        except socket.error:
            # Handle socket errors (e.g., client disconnects)
            print(f"Connection with {client_address} closed.")
            break
        '''
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        led.on() # Turn LED on

        # Send a welcome message to the client
        welcome_message = "Welcome to the chat server! Type 'bye' to exit.!"
        client_socket.send(welcome_message.encode())

        print(f"Type a message to start a conversation with {client_address}")

        

        #while True:
        # Check if there is data available for reading from the client socket
        readable, _, _ = select.select([client_socket], [], [], 0.1)

        if not readable :
            replyToClient(client_socket, readable)
             
        clientRead(client_socket, client_address)

        print(f"Connection with {client_address} closed.")
        client_socket.close()
        led.off() # Turn LED off
        '''


def clientRead(client_socket, client_address):
    # Receive data from the client
        data = client_socket.recv(1024)
        #if not data:
        #    break

        # Convert bytes to string
        received_message = data.decode()

        # Print the received message
        print(f"Received message from {client_address}: {received_message}")

        # Check if the client wants to exit
        #if received_message.lower() == 'bye':
        #    break

def replyToClient(client_socket, readable):
    if readable:
         return
    else:    
        # Get a response from the server user
        response_message = input("Your message: ")

        # Send the response back to the client
        client_socket.send(response_message.encode())




init()
loop()


    



'''
while True:
  
  time.sleep(1)
  led.off() # Turn the LED off
  time.sleep(1)  # Pause for 1 second
'''