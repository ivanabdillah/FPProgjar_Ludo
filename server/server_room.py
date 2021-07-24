import threading
from client import *
from server_play import *

class Room():
    numberid = 0
    def __init__(self, client):
        self.listclient = []
        self.playercount = 0
        self.id = Room.numberid
        Room.numberid += 1
        self.play = servGame()
        self.addclient(client)

    def addclient (self, client):
        self.listclient.append(client)
        self.playercount += 1
        client.addroom(self)
        self.checkplayer()

    def sendtoclient (self, client, message):
        print(client)
        for c in self.listclient:
            if c != client:
                print("c"+c)
                c.send(message)

    def checkplayer (self):
        if self.playercount == 4:
            self.play.play_game()

    def broadcast (self, message):
        for c in self.listclient:
            c.send(message)