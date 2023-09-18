RANKS = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King")
SUITS = ("Diamonds", "Hearts", "Spades", "Clubs")


class Card:


    rank = str()
    suit = str()


    def __init__(self, value, suit):
        self.suit = suit
        self.rank = value

    def card_string(self):
        return f"{self.rank} {self.suit}"

    def print(self):
        print(self.card_string())


    def get_value(self):
        if self.rank == "Ace":
            return 11
        elif self.rank in ("10", "Jack", "Queen", "King"):
            return 10
        else:
            return int(self.rank)
