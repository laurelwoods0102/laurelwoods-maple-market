import socket

HOST = 'laurelwoods-maple-market-engine'
PORT = 8887

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

client_socket.sendall("laurelwoods".encode())

data = client_socket.recv(1024)
print("Response : ", repr(data.decode()))

client_socket.close()