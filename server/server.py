from server_room import *
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
        self.prompt_end = "> "
        self.game = Game()
        # used for nicer print
        self.prompted_for_pawn = False
        # getting game data
        self.record_runner = None
        self.thread = threading.Thread(target=self.run, args=()).start()

  def handler(self, command, client):
        command = command.split("|")
        if command[0] == "room":
            if command[1] == "create":
                self.addroom(client)
            if command[1] == "join":
                self.joinroom(client)
            if command[1] == "chat":
                flag = 0
                for c in listclient:
                  if c == client:
                    flag = 1
                if flag == 0:
                  if len(listroomcli) == 0:
                    self.addchatroom(client)
                  else:
                    self.joinroomcli(client)
                for i in listclient:
                  if i != client:
                    if command[2] == 'Y':
                      i.send("Someone has entered chatroom!")
                    else:
                      i.send(command[2])
        if command[0] == "reset":
            for i in listclient:
              if i == client:
                listclient.remove(i)
            for c in listroomcli:
              listroomcli.pop()

  def run(self):
    while True:
        sock, addr = self.socket.accept()
        #buat client
        client = Client(sock, addr, self)

  def addchatroom (self,client):
    room = Room(client)
    print("has enter chat room")
    listroomcli.append(room)

  def joinroomcli(self, client):
    for room in listroomcli:
      if room.playercount < 4:
        print("has enter chat room")
        room.addclient(client)
    
  def addroom(self, client):
    room = Room(client)
    self.listroom.append(room)
    print("room is created")

  def joinroom(self, client):
    for room in self.listroom:
      if room.playercount < 4:
        print("has join the room")
        room.addclient(client)

server = Server()
# server.run