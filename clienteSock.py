import socket

HOST = "192.168.101.4"
PORT = 65123

with socket.socket(socket.AF_INET,socket.SOCK_STREAM)  as s:
    s.connect((HOST,PORT))
    
    s.sendall(b"hola mundo")
    data= s.recv(1024)
    print("Recibido".repr(data))
