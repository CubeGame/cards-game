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
    # n1 and n2 are assumed to have a length <= 8, It won't break if they do

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
        print("_\nTurn #{:d}".format(turn))

        sleep(1)
        print()

        cards = deck.pop(), deck.pop()
        card1, card2 = cards

        for i, name in enumerate(ns):
            print("{:>8} ({:>2}): {}".format(name, len(hs[i]), cards[i]))
            sleep(1)

        print()

        p1_win = bool(card1.against(card2))
        winner = 1 - int(p1_win)
        
        print("{} beats {}".format(card1, card2))
        hs[winner].extend(cards)
        
        sleep(1)
        
        print(ns[winner], "won")

        sleep(1)

    h1, h2 = hs
    l1, l2 = len(h1), len(h2)
    ls = l1, l2
    p1_outcome = Outcome.from_comparison(l1, l2)

    print("_\nTotals:")
    for i, name in enumerate(ns):
        print("{:>8}: {}".format(name, ls[i]))
        sleep(0.5)

    print()

    assert int(p1_outcome) in (1,2)
    winner = 2 - int(p1_outcome)

    print(ns[winner], "won!")
    print("Cards: ")
    for card in hs[winner]:
        print("*", card)
        sleep(0.5)

    return p1_outcome, l1, l2
