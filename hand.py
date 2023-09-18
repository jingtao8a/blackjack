from card import Card


class Hand:
    cards_in_hand = []
    is_stand = False
    is_double = False
    wager = 1

    def __init__(self):
        self.cards_in_hand = []

    def add_card(self, card):
        self.cards_in_hand.append(card)

    def print(self):
        lst_of_card_strings = []
        for item in self.cards_in_hand:
            lst_of_card_strings.append(item.card_string())
        print("\t".join(lst_of_card_strings))

    def is_blackjack(self):
        if len(self.cards_in_hand) != 2:
            return False
        return self.contains_ace() and self.score_tuple()[1] == 21

    def is_splittable(self):
        return len(self.cards_in_hand) == 2 and self.cards_in_hand[0].get_value() == self.cards_in_hand[1].get_value()

    def is_doubleable(self):
        return len(self.cards_in_hand) == 2

    def dealer_up_card(self):  # purpose of method is to hide dealer hidden card from player
        return self.cards_in_hand[0]

    def contains_ace(self):
        for card in self.cards_in_hand:
            if card.get_value() == 11:
                return True
        return False

    def is_21(self):
        return self.score_tuple()[1] == 21

    def is_bust(self):
        return self.score_tuple()[1] > 21

    # returns 2-tuple: str containing the hard/soft quality of the hand, int representing the hand's score)
    def score_tuple(self):
        score_value = 0
        number_of_aces = 0

        # Calculate the initial (greedy i.e. score(Ace) = 11) value of the hand
        for card in self.cards_in_hand:
            score_value += card.get_value()
            if card.rank == 'Ace':
                number_of_aces += 1

        # Adjust the value of Aces if necessary to make the hand soft
        while number_of_aces > 0 and score_value > 21:
            score_value -= 10
            number_of_aces -= 1

        if number_of_aces > 0:
            return "Soft", score_value
        else:
            return "Hard", score_value

    def score_string(self):
        return f"{self.score_tuple()[0]} {self.score_tuple()[1]}"

