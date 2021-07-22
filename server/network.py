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
        self.username()

        Thread(target=self.chat, args=()).start()  
        Thread(target=self.recv_msg, args=()).start()

    def send_msg(self, data):
        self.server.send(data.encode())

    def recv_msg(self):
        while True:
            data = self.server.recv(2048)
            print(data.decode())

    def username(self):
        data = "username|"
        data += input("username: ")
        self.send_msg(data)

    def chat(self):
        while True:
            data = input()
            data = data.split("|")
            if data[0] == "chat":
                self.send_msg("room|chat|" + data[1])
