from unittest import case
from game import Game
import tkinter as tk
from PIL import Image, ImageTk
from card import RANKS, SUITS
from BJ_leaderboard import update_leaderboard
from login import Login

class GUIGame(Game):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.root = tk.Tk()
        self.root.title("21点")
        self.blackjack_score = 0
        self.hand_score = 0
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()
        self.carImages = dict()
        for rank in RANKS:
            for suit in SUITS:
                self.carImages[rank + "_" + suit.lower()] = ImageTk.PhotoImage(Image.open("pukeImage/"+ rank + "_" + suit.lower() +".jpg"))
        self.hitButton = tk.Button(self.root, text="hit", command=lambda:self.hit())
        self.standButton = tk.Button(self.root, text="stand", command=lambda:self.stand())
        self.splitButton = tk.Button(self.root, text="split", command=lambda:self.split())
        self.doubleButton = tk.Button(self.root, text="double", command=lambda:self.double())
        self.continueButton = tk.Button(self.root, text="继续游戏", command=lambda:self.continueGame())
        self.quitButton = tk.Button(self.root, text="退出游戏", command=lambda:self.quitGame())

        self.stateLabel = tk.Label(self.root, text="游戏中", font=("Helvetica", 16))
        self.winerLabel = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.stateLabel.pack()
        self.winerLabel.pack()

    def play_hand(self):
        if self.username == "":
            print("no username")
            self.root.destroy()
            return
        print("username", self.username)
        # 1. blackjack_phase()
        self.updatePlayerCardImage()
        self.blackjack_score = self.blackjack_phase()
        self.hand_score = 0
        if self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack():
            if self.blackjack_score + self.hand_score > 0:
                print("Player wins", self.blackjack_score + self.hand_score, "unit(s).")
                self.winerLabel.configure(text="Player wins " + str(self.blackjack_score + self.hand_score) +  " unit(s).")
            elif self.blackjack_score + self.hand_score < 0:
                print("Player loses", -(self.blackjack_score + self.hand_score), "unit(s).")
                self.winerLabel.configure(text="Player loses " + str(-(self.blackjack_score + self.hand_score)) + " unit(s).")
            else:
                print("No net change in Player's total score.")
                self.winerLabel.configure(text="No net change in Player's total score.")
            self.leaderboard_score += (self.blackjack_score + self.hand_score)
            print("\n------------------------------------------------------------------------------------------\n")
            self.diplayFinalCardImage()
            self.displayContinueAndQuitButton()
        else:
            # 2. play_hand_loop() and 3.dealer_phase() 4.scoring_phase()
            self.play_hand_loop()

        self.root.mainloop()


    def play_hand_loop(self):
        self.updatePlayerCardImage()
        if not (self.player_hand.is_stand or self.player_hand.is_double or self.player_hand.is_21() or self.player_hand.is_bust()):
            print("Current Player hand: ")
            self.player_hand.print()
            print("Player has", self.player_hand.score_string(), "against Dealer", self.dealer_hand.dealer_up_card().rank)
            self.stateLabel.configure(text = "Player has " + self.player_hand.score_string() + " against Dealer " + self.dealer_hand.dealer_up_card().rank)
            self.updatePlayerOptions(self.player_options_list())
        else:
            self.updatePlayerOptions([])
            print("Current hand complete. The Player's cards are: ")
            self.player_hand.print()
            self.completed_hands.append(self.player_hand)
            if self.player_hand.is_21():
                print("Player has 21. ")
                self.stateLabel.configure(text = "Player has 21. ")
            elif self.player_hand.is_bust():
                print("Player has", self.player_hand.score_tuple()[1], "and is bust.")
                self.stateLabel.configure(text = "Player has " + str(self.player_hand.score_tuple()[1]) +  " and is bust.")
            else:
                print("Player has", self.player_hand.score_tuple()[1])
                self.stateLabel.configure(text = "Player has " + str(self.player_hand.score_tuple()[1]))

            if self.split_hands:
                self.split_hand_phase()
                return
            
            # 3.dealer_phase() 
            self.dealer_phase()

            # 4.scoring_phase()
            self.hand_score = self.scoring_phase()

            if self.blackjack_score + self.hand_score > 0:
                print("Player wins", self.blackjack_score + self.hand_score, "unit(s).")
                self.winerLabel.configure(text="Player wins " + str(self.blackjack_score + self.hand_score) +  " unit(s).")
            elif self.blackjack_score + self.hand_score < 0:
                print("Player loses", -(self.blackjack_score + self.hand_score), "unit(s).")
                self.winerLabel.configure(text="Player loses " + str(-(self.blackjack_score + self.hand_score)) + " unit(s).")
            else:
                print("No net change in Player's total score.")
                self.winerLabel.configure(text="No net change in Player's total score.")
            self.leaderboard_score += (self.blackjack_score + self.hand_score)
            print("\n------------------------------------------------------------------------------------------\n")
            self.diplayFinalCardImage()
            self.displayContinueAndQuitButton()
    
    def continueGame(self):
        self.hiddenContinueAndQuitButton()
        print("Playing next Blackjack hand.")
        self.winerLabel.config(text="")
        self.stateLabel.config(text="")
        self.initialization()
        self.play_hand()

    def quitGame(self):
        self.hiddenContinueAndQuitButton()
        print("You have exited the game. Your leaderboard score: ", self.leaderboard_score)
        self.winerLabel.config(text="You have exited the game. Your final score: " + str(self.leaderboard_score))
        self.stateLabel.config(text="")
        update_leaderboard(self.username, self.leaderboard_score)
        self.backButton = tk.Button(self.root, text="BackToLogin", command=lambda:self.backToLogin())
        self.backButton.pack()

    def backToLogin(self):
        self.root.destroy()
        login = Login()
        login.start()
        game = GUIGame(login.username)
        game.play_hand()

    def displayContinueAndQuitButton(self):
        self.continueButton.pack()
        self.quitButton.pack()
    
    def hiddenContinueAndQuitButton(self):
        self.continueButton.pack_forget()
        self.quitButton.pack_forget()

    def getCardImage(self, card):
        return self.carImages[card.rank + "_" + card.suit.lower()]
        
    def updatePlayerCardImage(self):
        player_cards = self.player_hand.cards_in_hand
        
        self.canvas.delete("all")
        for i in range(len(player_cards)):
            self.canvas.create_image((i + 1) * 40, 100, image=self.getCardImage(player_cards[i]), anchor="w")
        self.canvas.create_image(460, 100, image=self.getCardImage(self.dealer_hand.dealer_up_card()), anchor="w")
    
    def diplayFinalCardImage(self):
        player_cards = self.player_hand.cards_in_hand
        self.canvas.delete("all")
        for i in range(len(player_cards)):
            self.canvas.create_image((i + 1) * 40, 100, image=self.getCardImage(player_cards[i]), anchor="w")
        dealer_cards = self.dealer_hand.cards_in_hand
        for i in range(len(dealer_cards)):
            self.canvas.create_image(460 - i * 40, 100, image=self.getCardImage(dealer_cards[i]), anchor="w")
    
    def updatePlayerOptions(self, options):
        if "Hit" not in options:
            self.hitButton.pack_forget()
        else:
            self.hitButton.pack()

        if "Stand" not in options:
            self.standButton.pack_forget()
        else:
            self.standButton.pack()

        if "Split" not in options:
            self.splitButton.pack_forget()
        else:
            self.splitButton.pack()

        if "Double" not in options:
            self.doubleButton.pack_forget()
        else:
            self.doubleButton.pack()

    def stand(self):
        super().stand()
        self.play_hand_loop()

    def hit(self):
        super().hit()
        self.updatePlayerCardImage()
        self.play_hand_loop()

    def double(self):
        super().double()
        self.updatePlayerCardImage()
        self.play_hand_loop()
    
    def split(self):
        super().split()
        self.updatePlayerCardImage()
        self.play_hand_loop()
