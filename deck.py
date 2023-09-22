import random
from card import Card, RANKS, SUITS


class Deck:
    def __init__(self):
        self.cards = []
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def print(self):
        for card in self.cards:
            card.print()

    def deal(self):
        return self.cards.pop(0)
