#import and create a GUI
import tkinter
import tkinter.messagebox
from BJ_leaderboard import show_leaderboard

class Login:
    def __init__(self):
        self.username = ""
        self.root = tkinter.Tk()
        self.root.geometry("400x200")
        self.root.title("BlackJack")
        #Entry Widget to input user name    
        self.input_label = tkinter.Label(self.root, text="Please input your user name")
        self.input_label.pack()
        self.input_field = tkinter.Entry(self.root)
        self.input_field.pack()

        #Button for start, help, leaderboard
        BTN_start = tkinter.Button(self.root, text="START", command=lambda:self.user_start())
        BTN_start.place(x= 175, y= 60)

        BTN_help = tkinter.Button(self.root, text="HELP", command=lambda:self.user_help())
        BTN_help.place(x= 178, y= 110)

        BTN_leaderb = tkinter.Button(self.root, text="LEADERBOARD", command=lambda:self.user_leaderb())
        BTN_leaderb.place(x= 150, y= 160)

    #press start button to save user name and start a game
    def user_start(self):
        #start the game
        print("BlackJack Game")

        self.username = self.input_field.get()
        self.root.destroy()


    #press help button-show BlackJack rules
    def user_help(self):
        tkinter.messagebox.showinfo("Help", "BlackJack rules")
    

    #press leaderboard button-show the leaderboard
    def user_leaderb(self):
        info = show_leaderboard()
        tkinter.messagebox.showinfo("Leaderboard", info)

    def start(self):
        #start the GUI
        self.root.mainloop()