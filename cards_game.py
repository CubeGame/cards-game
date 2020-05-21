from cards_users import User, cli_login, cli_register, cli_delete
from cards_logic import play, Outcome

import os

class Menu:
    def __init__(self, name, options=dict()):
        self.name = str(name)
        self.options = {}
        for k, f in options.items():
            self.options[k.lower()] = f

        self.options["exit"] = lambda : 1
        
    def run(self):
        self.loop = True
        while self.loop:
            print("{}:".format(self.name))
            for o in self.options.keys():
                print("*", o)

            choice = input("> ").strip()
            if choice in self.options:
                print()
                o = self.options[choice]()
                if o == 1:
                    break
            else:
                print("That was not a valid command")
            print()
        print("Exited from menu")

    def __call__(self):
        return self.run()

    def exit(self): self.loop = False

def user_play():
    print("Play")

    players = []
    for i in (0,1):
        print("Player", i+1)
        player = cli_login()
        if player is None:
            print("Ending game")
            return
        else:
            players.append(player)

    if players[0] == players[1]:
        print("Can't use the same account")
        return
    
    p1_outcome, l1, l2 = play(n1=players[0].name, n2=players[1].name)

    if not os.path.isfile("hs.txt"):
        open("hs.txt", "w").close()

    highscores = []
    with open("hs.txt", "r") as f:
        for line in f.readlines():
            try:
                line = line.rstrip("\n")
                spl = line.split(",")
                highscores.append((spl[0], int(spl[1])))
            except:
                pass

    highscores.append((players[0].name, l1))
    highscores.append((players[1].name, l2))

    highscores = sorted(highscores, key=lambda x: x[1], reverse=True)

    print()
    print("Highscores: ")
    with open("hs.txt", "w") as f:
        for index, (name, score) in enumerate(highscores[:10]):
            print("{} {:>8} {:>2}".format(index+1, name, score))
            print(name, score, sep=",", file=f)

main = Menu("Main Menu", options={
    "register" : cli_register,
    "delete" : cli_delete,
    "play" : user_play
    })

main.run()
