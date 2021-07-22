from network import *
import threading
from client import *

class Room():
    numberid = 0
    def __init__(self, client):
        self.listclient = []
        self.playercount = 0
        self.id = Room.numberid
        Room.numberid += 1
        self.addclient(client)

    def addclient (self, client):
        self.listclient.append(client)
        self.playercount += 1
        client.addroom(self)
        self.checkplayer()


    def sendtoclient (self, client, message):
        for c in self.listclient:
            if c != client:
                c.send(message)

    def sendlooping (self,client,message):
        for c in self.listclient:
            if c == client:
                c.send(message)

    def checkplayer (self):
        if self.playercount == 4:
            i=0
            self.prompt_for_player(self.listclient)
            while True:
                if i == 4:
                    i = i-4
                self.sendlooping(self.listclient[i],"Your turn!")
                self.network.recv_msg
                i = i+1

    def broadcast (self, message):
        for c in self.listclient:
            c.send(message)