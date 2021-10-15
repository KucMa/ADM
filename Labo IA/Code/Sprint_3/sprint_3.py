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
        if self.nb_matches <= 0:
            return None, -1
        else:
            return self.nb_matches, 0

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
            system("cls")
            print("Le nombre d'allumettes doit être 1, 2 ou 3")
            action = input("Combien d'allumettes ?")

        return int(action)


class Random(Entity):
    def __init__(self, name):
        super().__init__(name)

    def get_action(self):
        return randint(1, 3)

class IA(Entity):
    def __init__(self, name, size, trainable):
        super().__init__(name)
        self.trainable = trainable
        self.V = {}
        self.reward = []
        self.eps = 0.99
        self.history = []
        for s in range(1, size+1):
            self.V[s] = 0.

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

def play(game, player1, player2, train = True):
    state = game.reset()
    players = [player1, player2]
    shuffle(players)
    p = 0
    while not game.is_finished():
        
        if type(players[p % 2]) == Human:
            game.display_matches()

        action = players[p % 2].get_action(state)
        n_state, reward = game.step(action)

        if reward != 0:
            player1[p % 2].lose_nb += 1 if reward == -1 else 0
            players[p % 2].win_nb += 1 if reward == 1 else 0
            players[(p + 1) % 2].lose_nb += 1 if reward == 1 else 0
            players[(p + 1) % 2].win_nb += 1 if reward == -1 else 0

        if p != 0 and type(players[(p + 1) % 2]) == IA:
            s, a, r, sp = players[(p + 1) % 2].history[-1]
            players[(p + 1) % 2].history[-1] = (s, a, reward * -1, n_state)

        players[p % 2].add_transition((state, action, reward, None))

        state = n_state
        p += 1

        if train:
            player1.train()
            player2.train()

if __name__ == '__main__':
    game = Game(12)

    p1 = IA("IA 1", game.nb_matches, True)
    p2 = IA("IA 2", game.nb_matches, True)

    random_player = Random("Random")
    human_player = Random("Natan")

    for i in range(0, 100000):
        if i % 10 == 0:
            p1.eps = max(p1.eps * 0.996, 0.05)
            p2.eps = max(p1.eps * 0.996, 0.05)
        play(game, p1, p2)
    p1.reset_stat()

    for key in p1.V:
        print(key, p1.V[key])
    print("--------------------------")

    for _ in range(0, 1000):
        play(game, p1, random_player, train=False)
    print("p1 win rate", p1.win_nb/(p1.win_nb + p1.lose_nb))
    #print("p1 win mean", np.mean(p1.rewards))

    while True:
        play(game, p1, human_player, train=False)