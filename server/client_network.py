import socket
from threading import Thread

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_address = '127.0.0.1'
        port = 8081
        self.server.connect((ip_address, port)) 
        Thread(target=self.recv_msg, args=()).start()

    def send_msg(self, data):
        # client to server
        self.server.send(data.encode())

    def recv_msg(self):
        # client from server
        while True:
            data = self.server.recv(2048)
            print(data.decode())