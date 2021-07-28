from server_room import *
from os import linesep
from client_network import *


class CLIGame():

    def __init__(self):
        self.prompt_end = "> "
        self.game = Game()
        # used for nicer print
        self.prompted_for_pawn = False
        # getting game data
        self.record_runner = None
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
                             "1 - join room",
                             "2 - enter chatroom"])
        choice = self.validate_input(text, int, (0, 1, 2))
        return choice

    def start(self):
        '''main method, starting cli'''
        try:
            while True:
                choice = self.get_user_initial_choice()
                if choice == 0:
                    self.network.send_msg("room|create")
                    break
                elif choice == 1:
                    self.network.send_msg("room|join")
                    break
                elif choice == 2:
                    print("Press 'Y' to enter chatroom!")
                    while True:
                        msgg = input()
                        print ("Masukkan pesan anda (untuk keluar ketikkan exit): ")
                        if msgg != "exit":
                            self.network.send_msg("room|chat|" + msgg)
                        else:
                            self.network.send_msg("reset")
                            break
            while True:
                msg = input()
                self.network.send_msg(msg)
        except (KeyboardInterrupt, EOFError):
            print(linesep + "Exit Game")


if __name__ == '__main__':
    CLIGame().start()
