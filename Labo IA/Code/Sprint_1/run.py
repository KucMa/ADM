from models import Game
from models import Player

import os as os

if __name__ == '__main__':
    player_1 = Player("Humain", input("Nom joueur 1 : "))
    player_2 = Player("Humain", input("Nom joueur 2 : "))
    os.system("cls")
    game = Game(player_1, player_2)

    game.play()