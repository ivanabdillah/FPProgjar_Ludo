from room import *
from client import Client
import socket
from threading import Thread
from game import Player, Game
from painter import present_6_die_name
from os import linesep
from network import *

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
      self.run()

  def handler(self, command, client):
      command = command.split("|")
      if command[0] == "room":
          if command[1] == "create":
            self.addroom(client)
            print("room is created")
          if command[1] == "join":
            self.joinroom(client)
            print(client,"has join the room")
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
  def __init__(self):
        
      self.network = Server()

  def validate_input(self, prompt, desire_type, allawed_input=None, error_mess="Invalid Option!", str_len=None):
      '''
      loop while receive correct value
      param allowed_input can be list of allowed values
      param str_len is two sized tuple if min and max
      '''
      prompt += linesep + self.prompt_end
      while True:
          choice = input(prompt)
          if not choice:
              print(linesep + error_mess)
              continue
          try:
              choice = desire_type(choice)
          except ValueError:
              print(linesep + error_mess)
              continue
          if allawed_input:
              if choice in allawed_input:
                  break
              else:
                  print("Invalid Option!")
                  continue
          elif str_len:
              min_len, max_len = str_len
              if min_len < len(choice) < max_len:
                  break
              else:
                  print(linesep + error_mess)
          else:
              break
      return choice

  def get_user_initial_choice(self):
      text = linesep.join(["choose option",
                            "0 - create room",
                            "1 - join room"])
      choice = self.validate_input(text, int, (0, 1))
      return choice

  def prompt_for_player(self):
      ''' get player attributes from input,
      initial player instance and
      add player to the game
      '''
      available_colours = self.game.get_available_colours()
      name = self.validate_input("Enter name for player", str, str_len=(1, 30))
      available_options = range(len(available_colours))
      if len(available_options) > 1:
          # show available colours
          options = ["{} - {}".format(index, colour)
                      for index, colour in
                      zip(available_options,
                      available_colours)]
          text = "choose colour" + linesep
          text += linesep.join(options)
          choice = self.validate_input(text, int, available_options)
          colour = available_colours.pop(choice)
      else:
          # only one colour left
          colour = available_colours.pop()
      player = Player(colour, name, self.prompt_choose_pawn)
      self.game.add_palyer(player)

  # def prompt_for_players(self):
  #     '''put all players in the game'''
  #     counts = ("first", "second", "third", "fourth last")
  #     text_add = "Add {} player"
  #     for i in range(2):
  #         print(text_add.format(counts[i]))
  #         self.prompt_for_player()
  #         print("Player added")

  #     text = linesep.join(["Choose option:",
  #                          "0 - add player",
  #                          "1 - start game with {} players"])
  #     for i in range(2, 4):
  #         choice = self.validate_input(text.format(str(i)), int, (0, 1))
  #         if choice == 1:
  #             break
  #         elif choice == 0:
  #             print(text_add.format(counts[i]))
  #             self.prompt_for_player()
  #             print("Player added")

  def prompt_choose_pawn(self):
      '''used when player (human) has more than
      one possible pawn to move.
      This method is pass as a callable during
      player instantiation
      '''
      text = present_6_die_name(self.game.rolled_value,
                                str(self.game.curr_player))
      text += linesep + "has more than one possible pawns to move."
      text += " Choose pawn" + linesep
      pawn_options = ["{} - {}".format(index + 1, pawn.id)
                      for index, pawn
                      in enumerate(self.game.allowed_pawns)]
      text += linesep.join(pawn_options)
      index = self.validate_input(
          text, int, range(1, len(self.game.allowed_pawns) + 1))
      self.prompted_for_pawn = True
      return index - 1

  def prompt_to_continue(self):
      text = "press Enter to continue" + linesep
      input(text)

  def print_players_info(self):
      word = "start" if self.game.rolled_value is None else "continue"
      print("Game {} with {} players:".format(
            word,
            len(self.game.players)))
      for player in self.game.players:
          print(player)
      print()

  def print_info_after_turn(self):
      '''it used game attributes to print info'''
      pawns_id = [pawn.id for pawn in self.game.allowed_pawns]
      # nicer print of dice
      message = present_6_die_name(self.game.rolled_value,
                                    str(self.game.curr_player))
      message += linesep
      if self.game.allowed_pawns:
          message_moved = "{} is moved. ".format(
              self.game.picked_pawn.id)
          if self.prompted_for_pawn:
              self.prompted_for_pawn = False
              print(message_moved)
              return
          message += "{} possible pawns to move.".format(
              " ".join(pawns_id))
          message += " " + message_moved
          if self.game.jog_pawns:
              message += "Jog pawn "
              message += " ".join([pawn.id for pawn in self.game.jog_pawns])
      else:
          message += "No possible pawns to move."
      print(message)

  def print_standing(self):
      standing_list = ["{} - {}".format(index + 1, player)
                        for index, player in enumerate(self.game.standing)]
      message = "Standing:" + linesep + linesep.join(standing_list)
      print(message)

  def print_board(self):
      print(self.game.get_board_pic())

  def play_game(self):
      '''mainly calling play_turn
      Game's method while game finished
      '''
      try:
          while not self.game.finished:
              self.game.play_turn()
              self.print_info_after_turn()
              self.print_board()
              self.record_maker.add_game_turn(
                  self.game.rolled_value, self.game.index)
              # self.prompt_to_continue()
          print("Game finished")
          self.print_standing()
          self.offer_save_game()
      except (KeyboardInterrupt, EOFError):
          print(linesep +
                "Exiting game. ")
          self.offer_save_game()
          raise

  def start(self):
      '''main method, starting cli'''
      try:
          choice = self.get_user_initial_choice()
          if choice == 0:  # start new game
              self.network.send_msg("room|create")
              self.prompt_for_player()
          elif choice == 1:
              self.network.send_msg("room|join")
              self.prompt_for_player()
      except (KeyboardInterrupt, EOFError):
          print(linesep + "Exit Game")

server = Server()
# server.run