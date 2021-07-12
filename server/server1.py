from room import *
from client import *
import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8081

class Server:
  def __init__(self):
      self.listclient = []
      self.listroom = []

      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.socket.bind((host, port))
      self.socket.listen(100)
      self.run()

  def handler(self, command, client):
      command = command.split("|")
      if command[0] == "room":
          if command[1] == "create":
            self.addroom(client)
            print("room is created")
          if command[1] == "join":
            self.joinroom(client)
            print("has join the room")
          if command[1] == "chat":
            client.chat(command[2])
            print(command[2])
      if command[0] == "username":
        client.username(command[1])
      if command[0] == "match":
        client.move(command[1])


  def run(self):
    while True:
      sock, addr = self.socket.accept()
      #buat client
      client = Client(sock, addr, self)
  
  def addroom(self, client):
    room = Room(client)
    self.listroom.append(room)

  def joinroom(self, client):
    for room in self.listroom:
      if room.playercount < 4:
        room.addclient(client)
        return

server = Server()
# server.run