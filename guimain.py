from guigame import GUIGame
from login import Login

if __name__ == '__main__':
    login = Login()
    login.start()
    game = GUIGame(login.username)
    game.play_hand()
