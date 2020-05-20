from enum import Enum
from random import shuffle, getrandbits
from time import sleep

class Card:
    def __init__(self, num, clr):
        self.num = num

        if isinstance(clr, int):
            clr = TriColor(clr)

        self.clr = clr

    def __str__(self): return "{} {}".format(self.clr, self.num)

    def against(self, other):
        if self.clr == other.clr:
            assert self.num != other.num
            return self.num if self.num > other.num else other.num
        else:
            return self.clr.against(other.clr)


class TriColor(Enum):
    RED, BLACK, YELLOW = 0, 1, 2

    def __str__(self): return self.name.capitalize()
    def __int__(self): return self.value

    def against(self, other):
        return Outcome((int(self) - int(other)) % 3)

class Outcome(Enum):
    DRAW, LOSE, WIN = 0, 1, 2

    def __bool__(self):
        o = self.abstract()
        if o is None: raise
        else: return o
        
    def __int__(self): return self.value

    def abstract(self):
        return {
            self.DRAW : None,
            self.LOSE : False,
            self.WIN : True
            }[self]

    def from_comparison(a, b):
        if a == b: return Outcome.DRAW
        elif a > b: return Outcome.WIN
        else: return Outcome.LOSE


def play(n1="Player 1", n2="Player 2"):
    if n1 == n2:
        print("Can't use the same name")
        return

    deck = [Card(n, c) for c in [0,1,2] for n in range(1,11)]
    shuffle(deck)

    ns = (n1, n2)
    hs = [[], []]

    turn = 0
    while len(deck) >= 2:
        turn += 1
        print("Turn #{:d}".format(turn))

        sleep(0.5)
        print()

        cards = deck.pop(), deck.pop()
        card1, card2 = cards

        for i, name in enumerate(ns):
            print("{}: {}".format(name, cards[i]))
            sleep(0.5)

        print()

        p1_win = bool(card1.against(card2))
        winner = 1 - int(p1_win)
        
        print("{} beats {}".format(card1, card2))
        hs[winner].extend(cards)
        
        sleep(0.5)
        
        print(ns[winner], "won")

        sleep(0.5)
        print()

    sleep(1)

    print("="*turn)

    h1, h2 = hs
    l1, l2 = len(h1), len(h2)
    ls = l1, l2
    p1_outcome = Outcome.from_comparison(l1, l2)

    print("Totals:")
    for i, name in enumerate(ns):
        print("{}: {}".format(name, ls[i]))
        sleep(0.5)

    print()

    if p1_outcome == Outcome.DRAW: # There is a 1 in 2^15 (32768) chance of this happening
        assert l1 == l2

        print("Drew:")
        print("Coin toss:")

        chooser = getrandbits(1)

        choose_heads = None
        while choose_heads is None:
            print("Player", chooser + 1, ": heads or tails?")
            ht = input("H/T: ").strip().upper()
            
            if ht in ("H", "HEAD", "HEADS"):
                choose_heads = True
            elif ht in ("T", "TAIL", "TAILS"):
                choose_heads = False
            else:
                print("That isn't a valid choice, try again")

        print("Tossing coin...")

        sleep(1)
        
        face_heads = getrandbits(1)
        if face_heads: print("HEADS!")
        else: print("TAILS!")
        print()

        winner = (chooser - choose_heads == face_heads) % 1
        
    else:
        assert int(p1_outcome) in (1,2)
        winner = 2 - int(p1_outcome)

    print(ns[winner], "won!")
    print("Cards: ")
    for card in hs[winner]:
        print("*", card)
        sleep(0.5)

    return p1_outcome, l1, l2
