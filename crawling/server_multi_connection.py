import socket 
from _thread import *

HOST = '0.0.0.0'
PORT = 8887

def threaded_socket(client_socket, addr):
    while True:
        try:
            data = client_socket.recv(1024)
            
            #if not data:
            #    print("...")
            
            if data:
                print(data.decode())
            client_socket.send(data)
        
        except ConnectionResetError as e:
            print("Socket Disconnected")
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

while True:
    client_socket, addr = server_socket.accept()
    start_new_thread(threaded_socket, (client_socket, addr))

  

client_socket.close()
server_socket.close()