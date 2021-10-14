import os
from random import randrange
from abc import ABCMeta, abstractmethod, ABC

class Entity(ABC):

    @property
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def name(self):
        pass

    def get_number_matches(self):
        pass

    
    def __init__(self, type, name):
        self.type = type
        self.name = name

class Player(Entity) :
    type = "Humain"
    def __init__(self, player_number):
        self.name =  input("Nom joueur : ")
        self.player_number = player_number
    
    def get_number_matches(self):
        nb_matches = int(input("Combien d'allumettes souhaitez-vous retirez (1, 2 ou 3) ? "))

        while (nb_matches < 1 or nb_matches > 3):
            print("Le nombres d'allumettes ne peut être que 1, 2 ou 3")
            nb_matches = int(input("Combien d'allumettes souhaitez-vous retirez (1, 2 ou 3) ? "))

        return nb_matches

class Random(Entity):
    type = "Random"
    def __init__(self, name, player_number):
        self.name =  name
        self.player_number = player_number
    
    def get_number_matches(self):
        return randrange(1, 3)

class IA(Entity) :
    type = "IA"
    def __init__(self):
        pass
    def get_number_matches(self):
        pass

class Game:

    def __init__(self, player_1, player_2):
        self.nb_matches = self.obtain_matches()
        self.player_1 = player_1
        self.player_2 = player_2
        self.round_number = 1
    
    def display_matches(self) :
       print("O " * self.nb_matches)
       print("| " * self.nb_matches)
       print("| " * self.nb_matches)
    
    def obtain_matches(self) :
        nb_matches = int(input("Combien d'allumettes pour la partie : "))
        while (nb_matches < 3 ):
            print("Le nombres d'allumettes ne peut être que 1, 2 ou 3")
            nb_matches = int(input("Combien d'allumettes pour la partie : "))
        return nb_matches

    def play(self):
        while self.nb_matches > 0:
            self.display_matches()
            print("Au tour de : ", self.player_1.name if self.round_number % 2 != 0 else self.player_2.name)
            self.nb_matches -= self.get_number_matches()
            self.round_number += 1
            os.system("cls")
            

        print("Le gagnant est :", self.player_1.name if self.round_number % 2 != 0 else self.player_2.name)