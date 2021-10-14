from abc import ABC, abstractmethod
from os import system
from random import randint, shuffle, uniform

class Game():

    def __init__(self, nb_matches):
        self.nb_matches = nb_matches
        self.nb_matches_original = nb_matches

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

    def step(self, nb_matches):
        nb_matches -= self.nb_matches

class Entity(ABC):

    @abstractmethod
    def __init__(self, name, num):
        self.name = name
        self.num = num
        self.win_nb = 0
        self.lose_nb = 0

    @abstractmethod
    def get_action(self):
        pass

    def reset_stat(self):
        self.win_nb = 0
        self.lose_nb = 0

class Human(Entity):
    def __init__(self, name, num):
        super().__init__(name, num)

    def get_action(self):
        action = input("Combien d'allumettes ?")
        while (action not in ['1', '2', '3']):
            system("cls")
            print("Le nombre d'allumettes doit être 1, 2 ou 3")
            action = input("Combien d'allumettes ?")

        return int(action)


class Random(Entity):
    def __init__(self, name, num):
        super().__init__(name, num)

    def get_action(self):
        return randint(1, 3)

class IA(Entity):
    def __init__(self, name, num, trainable):
        super().__init__(name, num)
        self.trainable = trainable
        self.V = {}
        self.reward = []
        self.eps = 0.99
        self.history = []

    def eps_greedy(self, state):
        actions = [1, 2, 3]
        vmin = None
        vi = None
        for i in range(0, 3):
            a = actions[i] 
            if state - a > 0 and (vmin is None or vmin > self.V[state - a]):
                vmin = self.V[state - a]
                vi = i
        return actions[vi if vi is not None else 1]

    def train(self):
        if not self.trainable:
            return

        for transition in reversed(self.history):
            s, a , r, sp = transition
            if r == 0:
                self.V[s] = self.V[s] + 0.001 * (self.V[sp] - self.V[s])
            else:
                self.V[s] = self.V[s] + 0.001 * (r - self.V[s])

        self.history = []

    def add_transition(self, n_tuple):
        self.history.append(n_tuple)
        s, a, r, sp = n_tuple
        self.reward.append(r)

    def get_action(self, state):
        if uniform(0, 1) < self.eps:
            action = randint(1, 3)
        else:
            action = self.eps_greedy(state)

        return action

def play(game, player1, player2, train):
    state = game.reset()
    players = [player1, player2]
    shuffle(players)
    p = 0
    while not game.is_finished():
        
        if players[p % 2].is_human: