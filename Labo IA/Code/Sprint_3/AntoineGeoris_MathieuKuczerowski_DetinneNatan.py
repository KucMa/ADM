from abc import ABC, abstractmethod
from os import system
from random import randint, random, shuffle, uniform

import numpy as np


class Game():

    def __init__(self, player1, player2, nb_matches = 12):
        self.nb_matches = nb_matches
        self.nb_matches_original = nb_matches
        self.player1 = player1
        self.player2 = player2

    def is_finished(self):
        if self.nb_matches <= 0:
            return True
        return False

    def reset(self):
        self.nb_matches = self.nb_matches_original

    def display_matches(self) :
       print("O " * self.nb_matches)
       print("| " * self.nb_matches)
       print("| " * self.nb_matches)

    def play(self, train):
        self.reset()
        players = [self.player1, self.player2]
        shuffle(players)
        p = 0

        while not self.is_finished():
            if isinstance(players[p % 2], Human):
                self.display_matches()

            state = self.nb_matches
            if isinstance(players[p % 2], AI):
                action = players[p % 2].get_action(self.nb_matches)
            else:
                action = players[p % 2].get_action()
            self.nb_matches -= action
            reward = -1 if self.nb_matches <= 0 else 0

            if isinstance(players[p % 2], AI):
                players[p % 2].add_transition((state, action, reward, None))

            if p != 0 and isinstance(players[(p + 1) % 2], AI):
                s, a, r, sp = players[(p + 1) % 2].history[-1]
                players[(p + 1) % 2].history[-1] = (s, a, reward * -1, self.nb_matches)
                   
            p += 1

        players[p % 2].win_nb += 1
        players[(p + 1) % 2].lose_nb += 1

        if isinstance(players[p % 2], Human) or isinstance( players[(p + 1) % 2], Human):
            print(players[p % 2].name)

        if train:
            self.player1.train()
            self.player2.train()
        

class Entity(ABC):

    @abstractmethod
    def __init__(self, name):
        self.name = name
        self.win_nb = 0
        self.lose_nb = 0

    @abstractmethod
    def get_action(self):
        pass

    def reset_stat(self):
        self.win_nb = 0
        self.lose_nb = 0

class Human(Entity):
    def __init__(self, name):
        super().__init__(name)

    def get_action(self):
        action = input("Combien d'allumettes ?")
        while (action not in ['1', '2', '3']):
            print("Le nombre d'allumettes doit être 1, 2 ou 3")
            action = input("Combien d'allumettes ?")

        return int(action)


class Random(Entity):
    def __init__(self, name):
        super().__init__(name)

    def get_action(self):
        return randint(1, 3)

class AI(Entity):
    def __init__(self, name, size, trainable = True):
        super().__init__(name)
        self.history = []
        self.V = {}
        for s in range(1, size+1):
            self.V[s] = 0.
        self.rewards = []
        self.eps = 0.99
        self.trainable = trainable

    def reset_stat(self):
        super().reset_stat()
        self.rewards = []

    def eps_greedy(self, nb_matches):
        actions = [1, 2, 3]
        vmin = None
        vi = None
        for i in range(0,3):
            action = actions[i]
            if nb_matches - action > 0 and (vmin is None or vmin > self.V[nb_matches - action]):
                vmin = self.V[nb_matches - action]
                vi  = i
        return actions[vi if vi is not None else 1]

    def get_action(self, nb_matches):
        if uniform(0, 1) < self.eps:
            return randint(1, 3)
        
        return self.eps_greedy(nb_matches)

    def add_transition(self, n_tuple):
        self.history.append(n_tuple)
        s, a, r, sp = n_tuple
        self.rewards.append(r)

    def train(self):
        if self.trainable:
            for transition in reversed(self.history):
                s, a, r, sp = transition
                if r == 0:
                    self.V[s] = self.V[s] + 0.001 * (self.V[sp] - self.V[s])
                else:
                    self.V[s] = self.V[s] + 0.001 * (r - self.V[s])
            self.history = [] 

if __name__ == "__main__":
    human_player = Human("Natan")
    random_player = Random("Random")
    ai1 = AI("IA1", 12)
    ai2 = AI("IA2", 12)

    game = Game(ai1, ai2)

    for i in range(25000):
        if (i % 15 == 0):
            ai1.eps = max(ai1.eps * 0.997, 0.05)
            ai2.eps = max(ai2.eps * 0.997, 0.05)
        game.play(True)

    file = open("ia_value_fonction.txt", "w")
    for key in ai1.V:
        file.write(str(key))
        file.write("\t")
        file.write(str(ai1.V[key]))
        file.write("\n")
    file.close()

    game.player2 = random_player
    
    ai1.reset_stat()
    for i in range(0, 1000):
        game.play(False)
    print("p1 win rate", ai1.win_nb/(ai1.win_nb + ai1.lose_nb))
    print("p1 win mean", np.mean(ai1.rewards))

    
    game.player2 = human_player

    while True:
        system("cls")
        game.play(False)
        if input("New game ? ") == 'n':
            break

