from server_room import *
import threading

# numberid = 0

class Client():
    numberid = 0
    def __init__(self, socket, addr, server):
        self.socket = socket
        self.addr = addr
        self.server = server
        self.id = Client.numberid
        self.BUFFER_SIZE = 2048
        Client.numberid += 1

        self.thread = threading.Thread(target=self.run, args=()).start()

    #server
    def run(self):
        while True:
            try:
                # server menerima pesan dari klien
                command = self.socket.recv(self.BUFFER_SIZE).decode()
                print(command)
                self.server.handler(command, self)
            except Exception as e:
                continue

    def username(self, username):
        self.username = username

    def send(self, message):
        self.socket.send(message.encode())

    def addroom(self, room):
        self.room = room

    def chat(self, chat):
       self.room.sendtoclient(self, self.username + "|" + chat)
    
    def move(self, move):
       self.room.sendtoclient(self, "match|" + self.username + "|" + move)
