import socket
import select
import sys
from threading import Thread

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_address = '127.0.0.1'
        port = 8081
        self.server.connect((ip_address, port))

        # Thread(target=self.chat, args=()).start()  
        Thread(target=self.recv_msg, args=()).start()

    def send_msg(self, data):
        # klien mengirim pesan ke server
        self.server.send(data.encode())

    def recv_msg(self):
        # klien menerima pesan dari server
        while True:
            data = self.server.recv(2048)
            print(data.decode())

    def chat(self):
        data = input("masukkan pesan anda: ")
        self.send_msg("room|chat|" + data)
