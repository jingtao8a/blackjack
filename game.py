from deck import Deck
from hand import Hand


class Game:

    def __init__(self):
        self.leaderboard_score = 0
        self.initialization()
        
    def initialization(self):
        self.prompt = True

        #  list to store the hands that occur after the split
        self.split_hands = []

        #  list to store completed hands to be evaluated at showdown
        self.completed_hands = []

        self.player_stands = False

        #  create Deck and initialize player hands
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        #  randomize order of deck
        self.deck.shuffle()

        # (Testing block): force values for ___
        # ace = Card("Ace", "Spades") # force values for blackjack
        # ten = Card("Queen", "Spades") # force values for blackjack
        # self.player_hand.add_card(Card("8", "Spades"))  # force values for split
        # self.player_hand.add_card(Card("8", "Hearts")) # force values for split

        # continue real gameplay

        # deal two cards to player
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())

        # deal first two cards to dealer (there is a method called hand.up_card() that covers up the second card
        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

    # Daniel Note: allows for loop to play hands indefinitely at user's input
    def play_prompt(self):
        player_play = input("Deal blackjack? (Y/N)\n")
        if player_play == "Y":
            print("Playing next Blackjack hand.")
            self.initialization()
            return self.play_hand()
        elif player_play == "N":
            print("You have exited the game. Your final score:", self.leaderboard_score)
            return False
        else:
            print("Invalid input")
            return self.play_prompt()

    # game object runs its main phases through the play_hand method
    # 1. blackjack_phase(): Program checks for Blackjack in both Player and Dealer's starting hands
    # 2. play_hand_loop(): If neither user has blackjack, program enters hand play
    # 3. dealer_phase(): Once Player completes his hand(s), Dealer hits until hard 17 or soft/hard 18+
    # 4. scoring_phase(): Program compares Player's list of hand(s) to the Dealer's hand, collectively scores them
    def play_hand(self):
        blackjack_score = self.blackjack_phase()
        hand_score = 0
        if not self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack():
            self.play_hand_loop()
            self.dealer_phase()
            hand_score = self.scoring_phase()

        if blackjack_score + hand_score > 0:
            print("Player wins", blackjack_score + hand_score, "unit(s).")
        elif blackjack_score + hand_score < 0:
            print("Player loses", -(blackjack_score + hand_score), "unit(s).")
        else:
            print("No net change in Player's total score.")
        self.leaderboard_score += (blackjack_score + hand_score)
        print("\n------------------------------------------------------------------------------------------\n")
        self.play_prompt()
    # 1. blackjack_phase(): Program checks for Blackjack in both Player and Dealer's starting hands
    # Returns the amount the Player's net win
    def blackjack_phase(self):
        # show both of Player's cards and one of Dealer's cards
        print("Player hand: ")
        self.player_hand.print()
        print("Dealer up card: ")
        self.dealer_hand.dealer_up_card().print()

        # case 1: both players have Blackjack
        if self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
            print("Player has blackjack. Checking if Dealer has Blackjack.")
            self.dealer_hand.print()
            print("Player and Dealer both have Blackjack. Player and dealer push.")
            return 0
        # case 2: only Player has Blackjack
        elif self.player_hand.is_blackjack():
            print("Player has blackjack. Checking if Dealer has Blackjack.")
            self.dealer_hand.print()
            print("Only Player has Blackjack.")
            return 1.5 * self.player_hand.wager
        # case 3: only Dealer has Blackjack
        elif self.dealer_hand.dealer_up_card().get_value() >= 10 and self.dealer_hand.is_blackjack():
            print("Checking if Dealer has Blackjack...")
            self.dealer_hand.print()
            print("Dealer has blackjack.")
            return -1 * self.player_hand.wager
        else:
            print("Neither Player or Dealer have Blackjack. Proceed to play phase.\n")
            return 0

    def play_hand_loop(self):
        # there are 4 conditions in which a player hand terminates

        # the following loop should terminate when any of the 4 conditions occur, any of which would end the hand
        # player_hand.is_stand returns False until Player stands, is modified in stand()
        # player_hand.is_double returns False until Player doubles, is modified in double()
        # player_hand.is_21() returns False until Player achieves a hand score of exactly 21
        # player_hand.is_bust() returns False until Player achieves a hand score of strictly greater than 21
        while not (
                self.player_hand.is_stand or self.player_hand.is_double or self.player_hand.is_21() or self.player_hand.is_bust()):
            # print("Split hands list (testing)", self.split_hands)
            print("Current Player hand: ")
            self.player_hand.print()
            print("Player has", self.player_hand.score_string(), "against Dealer",
                  self.dealer_hand.dealer_up_card().rank)
            self.print_player_options_string()
            input = self.receive_valid_int_input()  # input receives strictly valid input corresponding to valid options
            self.print_selected_option(input)
            self.execute_selected_option(input)  # executes selected options hit, stand, double or split when applicable
        # (Testing block)
        # print("(Testing) Hand stored in completed_hands list")
        # self.player_hand.print()
        print("Current hand complete. The Player's cards are: ")
        self.player_hand.print()

        # a complete hand will be stored in a new list to allow a split hand to occupy self.player_hand memory
        self.completed_hands.append(self.player_hand)
        # print("Player has", self.player_hand.score_string(), "against Dealer", self.dealer_hand.up_card().rank)
        if self.player_hand.is_21():
            print("Player has 21. ")
        elif self.player_hand.is_bust():
            print("Player has", self.player_hand.score_tuple()[1], "and is bust.")
        else:
            print("Player has", self.player_hand.score_tuple()[1])
        self.split_hand_phase()  # checks if the list of split hands is empty, plays each hand until list is empty

    # checks if the list of split hands is empty, plays each hand until list is empty
    def split_hand_phase(self):
        if self.split_hands:
            print("Playing the next split hand.\n")
            self.player_stands = False
            self.player_hand.is_double = False
            self.player_hand = self.split_hands.pop()
            # self.player_hand.print()
            # print("self.split_hands", self.split_hands)
            self.play_hand_loop()
        else:
            print("All hands are complete. Entering dealer phase\n")

    # 3. dealer_phase(): Once Player completes his hand(s), Dealer hits until hard 17 or soft/hard 18+
    def dealer_phase(self):
        print("Dealer has: ")
        self.dealer_hand.print()
        while self.dealer_hand.score_tuple()[1] < 17 or self.dealer_hand.score_tuple() == ("Soft", 17):
            self.dealer_hand.add_card(self.deck.deal())
            print("Dealer hits. Dealer hand is now:")
            self.dealer_hand.print()
            print("Dealer has: ", self.dealer_hand.score_string())

        print("Dealer phase ends.\n")
        if self.dealer_hand.is_bust():
            print("Dealer has", self.dealer_hand.score_tuple()[1], "and is bust.")
        else:
            print("Dealer has", self.dealer_hand.score_tuple()[1])
        print("Proceeding to scoring phase\n")

    def scoring_phase(self):
        total_change_in_score = 0
        statement = []
        for hand in self.completed_hands:
            net_score = 1
            print("Player has", hand.score_tuple()[1], "against Dealer", self.dealer_hand.score_tuple()[1])
            if hand.is_double:
                net_score *= 2
                statement.append("Player doubled\t")
            if hand.is_bust():
                net_score *= -1
                statement.append("Player is bust. Player loses\n")
            elif self.dealer_hand.is_bust():
                statement.append("Dealer is bust and Player is not bust. Player wins\n")
            elif hand.score_tuple()[1] > self.dealer_hand.score_tuple()[1]:
                statement.append("Player hand is better than Dealer hand. Player wins\n")
            elif hand.score_tuple()[1] < self.dealer_hand.score_tuple()[1]:
                net_score *= -1
                statement.append("Dealer hand is better than Player hand. Player loses\n")
            else:
                net_score = 0
                statement.append("Player hand is equivalent to Dealer hand. Player pushes\n")
            total_change_in_score += net_score
            print("\t".join(statement))
            statement.clear()
        return total_change_in_score

    def next_hand_prompt(self):
        pass

    def print_player_options_string(self):
        options_string_list = []
        for option_number, option in enumerate(self.player_options_list()):
            options_string_list.append(f"Enter {option_number} to {option}")
        print("\t".join(options_string_list))

    def receive_valid_int_input(self):
        valid_input = list(range(0, len(self.player_options_list())))
        try:
            selected_option = input()
            if int(selected_option) in valid_input:
                return int(selected_option)
            else:
                print("User input invalid. Try inputting again")
        except ValueError:
            print("User input invalid. Try inputting again")
        return self.receive_valid_int_input()

    def print_selected_option(self, int_input):
        print("You have selected to", self.player_options_list()[int_input])

    # returns Player's play options in the appropriate game state
    def player_options_list(self):
        player_options = ["Hit", "Stand"]
        if self.player_hand.is_splittable():
            player_options.append("Split")
        if self.player_hand.is_doubleable():
            player_options.append("Double")
        return player_options

    # takes in correct user input, executes selected options hit, stand, double or split when applicable
    def execute_selected_option(self, int_input):
        if int_input == self.player_options_list().index("Hit"):
            self.hit()
        elif int_input == self.player_options_list().index("Stand"):
            self.stand()
        elif int_input == self.player_options_list().index("Double"):
            self.double()
        elif int_input == self.player_options_list().index("Split"):
            self.split()

    # Player's options methods

    # no changes to Player's hand, current hand ends
    def stand(self):
        self.player_hand.is_stand = True

    # Player draws one card from Deck object at random
    def hit(self):
        self.player_hand.add_card(self.deck.deal())

    # Player elects to double the wager at beginning of current hand and hits one card, forfeiting subsequent hits
    def double(self):
        self.player_hand.is_double = True
        self.player_hand.add_card(self.deck.deal())

    # Player proceeds with current hand with his first card, then awaits a second hand with his second card of same rank
    def split(self):
        split_hand = Hand()
        split_hand.add_card(self.player_hand.cards_in_hand.pop())
        self.player_hand.add_card(self.deck.deal())
        split_hand.add_card(self.deck.deal())
        self.split_hands.append(split_hand)
