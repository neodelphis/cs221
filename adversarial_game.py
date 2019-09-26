# -*- coding: utf-8 -*-
# python 3.7

# -----------------------------------
# Modèle du jeu
# -----------------------------------


class HalvingGame:
    """
    HalvingGame : N allumettes Chaque joueur a tour à tour l'option
    de retirer 1 allumette ou de retirer la moitié de celles qui restent
    Le vainqueur est celui qui commence son tour avec 0

    state : (player, number) : joueur en cours, nb d'allumettes restantes
    player : +1 or -1
    """

    def __init__(self, N):
        self.N = N

    def startState(self):
        return (+1, self.N)

    def actions(self, state):
        # player, number = state
        return ['-', '/']

    def successor(self, state, action):
        player, number = state
        if action is '-':
            return (-player, number - 1)
        elif action is '/':
            return (-player, number // 2)
        assert False

    def isEnd(self, state):
        player, number = state
        return number == 0

    def utility(self, state):
        player, number = state
        # utility est seulement valide au dernier état
        assert self.isEnd(state)
        return player * float('inf')

    def player(self, state):
        player, number = state
        return player


# -----------------------------------
# Policy (stratégie)
# -----------------------------------


def simple_policy(game, state):
    action = '-'
    print('tour {}: l\'ordinateur choisit {} '.format(state, action))
    return action


def human_policy(game, state):
    while True:
        action = input(
            'tour {}: entrer l\'action choisie - ou / : '.format(state))
        if action in game.actions(state):
            return action


def minimax_policy(game, action):
    """
    Compute the value at a given state as well as what is the optimal action
    """
    def recurse(state):
        # return (utility of that state, action that achieves that utility)
        if game.isEnd(state):
            return (game.utility(state), None)
        # Candidates =  list of pairs of
        #               utility of successor state and action leading to that successor
        candidates = [
            (recurse(game.successor(state, action))[0], action)
            for action in game.actions(state)
        ]
        if player == +1:
            return max(candidates)
        elif player == -1:
            return min(candidates)
        assert False

    utility, action = recurse(state)
    print('minimax policy: state {} => action {} with utility {}'.format(
        state, action, utility))

    return action

# -----------------------------------
# Tours de jeu
# -----------------------------------


game = HalvingGame(N=15)
# print game.successor(game.startState(), '/')

policies = {
    +1: human_policy,
    # -1: simple_policy,
    -1: minimax_policy,
}

state = game.startState()
while not game.isEnd(state):
    player = game.player(state)  # Joueur qui contrôle l'état en cours
    policy = policies[player]  # Stratégie du joueur
    action = policy(game, state)  # Action en suivant la stratégie
    state = game.successor(state, action)  # Définition de l'état suivant
print(game.utility(state))
