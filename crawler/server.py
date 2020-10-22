import socket 

HOST = '0.0.0.0'
PORT = 8887

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(1)
client_socket, addr = server_socket.accept()

while True:
    data = client_socket.recv(1024)
    
    if not data:
        print("...")
    
    print(data.decode())
    client_socket.sendall(data)

client_socket.close()
server_socket.close()