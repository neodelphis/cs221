# -*- coding: utf-8 -*- 
from __future__ import division # Force les divisions d'entiers à être des rééls
import util, math, random
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.
class CounterexampleMDP(util.MDP):
    # Return a value of any type capturing the start state of the MDP.
    def startState(self):
        return 'start'

    # Return a list of strings representing actions possible from |state|.
    def actions(self, state):
        results = []
        if state is 'start':
            results.append('chance') # Chance node
            results.append('sure')   # Chance node with 100% prob
        return results

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # Remember that if |state| is an end state, you should return an empty list [].
    def succAndProbReward(self, state, action):
        results = []  # (newState, prob, reward)
        if action is 'chance':
            results.append(('end', 0.8, 2))
            results.append(('end', 0.2, 6))
        elif action is 'sure':
            results.append(('end', 1, 3))
        return results

    # Set the discount factor (float or integer) for your counterexample MDP.
    def discount(self):
        return 0

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: list of integers (face values for each card included in the deck)
        multiplicity: single integer representing the number of cards with each face value
        threshold: maximum number of points (i.e. sum of card values in hand) before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look closely at this function to see an example of state representation for our Blackjack game.
    # Each state is a tuple with 3 elements:
    #   -- The first element of the tuple is the sum of the cards in the player's hand.
    #   -- If the player's last action was to peek, the second element is the index
    #      (not the face value) of the next card that will be drawn; otherwise, the
    #      second element is None.
    #   -- The third element is a tuple giving counts for each of the cards remaining
    #      in the deck, or None if the deck is empty or the game is over (e.g. when
    #      the user quits or goes bust).
    #      Ca aurait pê été mieux d'utiliser une liste...
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be placed into the succAndProbReward function below.
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']


    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # A few reminders:
    # * Indicate a terminal state (after quitting, busting, or running out of cards)
    #   by setting the deck to None.
    # * If |state| is an end state, you should return an empty list [].
    # * When the probability is 0 for a transition to a particular new state,
    #   don't include that state in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        """
        Renvoie une liste `results` de (new_state, probability, reward) où
        new_state   : s', état dans lequel on peut arriver
        probability : T(s,a,s')
        reward      : Reward(s,a,s')

        state : ( total_card_value_in_hand ,
                  next_card_index_if_peeked,
                  deck_card_count )
        deck_card_count : liste dont l'index correspond à la valeur de la carte dans la liste `card_values 
                          et le nombre correspond au nb de cartes de ce type restantes dans la pioche 
        """
        results = []

        total_card_value_in_hand , next_card_index_if_peeked, deck_card_count = state

        # Les fonctions utiles
        # Savoir si on se trouve dans un état final
        # def isEnd(state):
        #     _ , _, deck_card_count = state
        #     return deck_card_count == None

        # # Montre une carte de la pioche
        # def next_card(deck_card_count):
        #     # renvoie aléatoirement une carte représentée par son index
        #     # Reconstruction du deck
        #     deck = []
        #     for index, card_count in enumerate(deck_card_count):
        #         # index : hauteur de la carte
        #         # card_count : nd de cartes de ce type restant dans le deck
        #         deck += list((index,)*card_count)
        #     return random.choice(deck_card_count)   

        # --- Corps principal de la fonction succAndProbReward --- #
        # Cas d'un état final
        # empy_list = []
        if deck_card_count == None:
            return results  # Liste vide

        # On est forcé de quitter le jeu s'il n'y a plus de cartes dans la pioche
        # s' : end
        # T  : 1, pas de choix d'action
        # R  : valeur des cartes en main
        if sum(deck_card_count) == 0:
            end_state = (total_card_value_in_hand, None, None)
            probability = 1
            reward = total_card_value_in_hand
            results.append((end_state, probability, reward))
            return results

        # On quitte de son propre gré
        if action == 'Quit':
            end_state = (total_card_value_in_hand, None, None)
            probability = 1
            reward = total_card_value_in_hand
            results.append((end_state, probability, reward))
            return results

        # Il reste des cartes dans la pioche et on n'a pas quitté
        # Construction de la liste des successeurs possibles
        if action == 'Peek':
            # s' : même état avec `next_card_index_if_peeked` modifié
            # T  : probablité de voir une carte de hauteur donnée
            # R  : - peekCost

            # Probabilité de voir apparaître une carte lorsqu'on en regarde une au hasard
            number_of_cards = sum(deck_card_count)
            peek_probability = tuple(card_count/number_of_cards for card_count in deck_card_count)

            # Liste des états atteignables
            for index, probability in enumerate(peek_probability):
                if probability != 0:
                    new_state = ( total_card_value_in_hand , index, deck_card_count )
                    # probability récupéré directement dans l'enum
                    reward = - self.peekCost
                    results.append((new_state, probability, reward))

            return results


        # On choisi de prendre une carte
        if action == 'Take':

            # Cas où l'on n'a pas regardé de carte le tour précédent
            if next_card_index_if_peeked == None:
                # On pioche une carte
                # deux cas de figure:
                # 1- Elle est de valeur trop haute et la somme des cartes de notre main est supérieure au seuil
                #    on a une récompense totale de 0 et on est dirigé vers un état final
                # 2- Elle n'est pas trop haute et on peut continuer le jeu 
                #    sauf s'il ne reste plus de cartes dans la pioche

                number_of_cards = sum(deck_card_count)

                # 1- On pioche une carte trop haute

                # Nombre de cartes trop hautes dans la pioche
                # number_of_bust_cards = sum( card_count for index, card_count in enumerate(deck_card_count)
                #                             if self.cardValues[index] > (self.threshold - total_card_value_in_hand) )
                # if number_of_bust_cards > 0:
                #     new_state = ( 0 , None, None )
                #     probability = number_of_bust_cards / number_of_cards
                #     reward = 0
                #     results.append((new_state, probability, reward))

                # 2- On pioche une carte dont la valeur ne nous fais pas dépasser le seuil
                for index, card_count in enumerate(deck_card_count):
                    # if self.cardValues[index] <= (self.threshold - total_card_value_in_hand):
                        # On estime la probabilité d'obtenir cardValues[index]
                        # Seulement pour les cartes présentes dans la pioche
                    if card_count > 0:
                        new_total_card_value_in_hand = total_card_value_in_hand + self.cardValues[index]
                        probability = card_count / number_of_cards
                        reward = 0
                        # 1- On pioche une carte trop haute
                        if new_total_card_value_in_hand > self.threshold:
                            new_state = ( new_total_card_value_in_hand ,
                                          None,
                                          None ) 
                        # 2- On pioche une carte dont la valeur ne nous fais pas dépasser le seuil
                        else:
                            list_card_count = list(deck_card_count)
                            list_card_count[index] -= 1
                            new_deck_card_count = tuple(list_card_count)  # Bof bof de travailler avec des tuples
                            # Prise en compte du cas où l'on vide la pioche
                            # La récompense devient la main en cours et fin
                            if sum(new_deck_card_count) == 0:
                                new_deck_card_count = None
                                reward = new_total_card_value_in_hand
                            new_state = ( new_total_card_value_in_hand ,
                                          None,
                                          new_deck_card_count )
                          
                        
                        results.append((new_state, probability, reward))


                # for index, card_count in enumerate(deck_card_count):
                #     if self.cardValues[index] <= (self.threshold - total_card_value_in_hand):
                #         # On estime la probabilité d'obtenir cardValues[index]
                #         # Seulement pour les cartes présentes dans la pioche
                #         if card_count > 0:
                #             probability = card_count / number_of_cards
                #             print('-'*80)
                #             print probability
                #             print('-'*80)
                #             list_card_count = list(deck_card_count)
                #             list_card_count[index] -= 1
                #             new_deck_card_count = tuple(list_card_count)  # Bof bof de travailler avec des tuples
                #             new_state = ( total_card_value_in_hand + self.cardValues[index] ,
                #                           None,
                #                           new_deck_card_count )
                #             reward = 0
                #             results.append((new_state, probability, reward))


            # Cas où l'on a regardé une carte le tour précédent
            else:  # next_card_index_if_peeked != None
                number_of_cards = sum(deck_card_count)

                # 1- On pioche une carte trop haute - Bon un peu bête dans ce cas, mais bon on sais jamais
                if self.cardValues[next_card_index_if_peeked] > (self.threshold - total_card_value_in_hand):
                    new_state = ( 0 , None, None )
                    probability = 1
                    reward = 0
                    results.append((new_state, probability, reward))
                # 2- On pioche une carte dont la valeur ne nous fais pas dépasser le seuil
                else :
                    probability = 1
                    list_card_count = list(deck_card_count)
                    list_card_count[next_card_index_if_peeked] -= 1
                    new_deck_card_count = tuple(list_card_count)  # Bof bof de travailler avec des tuples
                    new_state = ( total_card_value_in_hand + self.cardValues[next_card_index_if_peeked] ,
                                  None,
                                  new_deck_card_count )
                    reward = 0
                    results.append((new_state, probability, reward))                

                # Nombre de cartes trop hautes dans la pioche
                # number_of_bust_cards = sum( card_count for index, card_count in enumerate(deck_card_count)
                #                             if cardValues[index] > (threshold - total_card_value_in_hand) )
                # if number_of_bust_cards > 0:
                #     new_state = ( 0 , None, None )
                #     probability = number_of_bust_cards / number_of_cards
                #     reward = 0
                #     results.append((new_state, probability, reward))

                # # 2- On pioche une carte dont la valeur ne nous fais pas dépasser le seuil
                # for index, card_count in enumerate(deck_card_count):
                #     if cardValues[index] <= (threshold - total_card_value_in_hand):
                #         # On estime la probabilité d'obtenir cardValues[index]
                #         # Seulement pour les cartes présentes dans la pioche
                #         if card_count > 0:
                #             probability = card_count / number_of_cards

                #             list_card_count = list(deck_card_count)
                #             list_card_count[index] -= 1
                #             new_deck_card_count = tuple(list_card_count)  # Bof bof de travailler avec des tuples
                #             new_state = ( total_card_value_in_hand + cardValues[index] ,
                #                           None,
                #                           new_deck_card_count )
                #             reward = 0
                #             results.append((new_state, probability, reward))

            # Dans tous les cas
            return results


        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action at least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning
# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)

def simulate_QL_over_MDP(mdp, featureExtractor):
    # NOTE: adding more code to this function is totally optional, but it will probably be useful
    # to you as you work to answer question 4b (a written question on this assignment).  We suggest
    # that you add a few lines of code here to run value iteration, simulate Q-learning on the MDP,
    # and then print some stats comparing the policies learned by these two approaches.
    # BEGIN_YOUR_CODE
    pass
    # END_YOUR_CODE


############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs.
# (See identityFeatureExtractor() above for a simple example.)
# Include the following features in the list you return:
# -- Indicator for the action and the current total (1 feature).
# -- Indicator for the action and the presence/absence of each face value in the deck.
#       Example: if the deck is (3, 4, 0, 2), then your indicator on the presence of each card is (1, 1, 0, 1)
#       Note: only add this feature if the deck is not None.
# -- Indicators for the action and the number of cards remaining with each face value (len(counts) features).
#       Note: only add these features if the deck is not None.
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state

    # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 4d: What happens when the MDP changes underneath you?!

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)

def compare_changed_MDP(original_mdp, modified_mdp, featureExtractor):
    # NOTE: as in 4b above, adding more code to this function is completely optional, but we've added
    # this partial function here to help you figure out the answer to 4d (a written question).
    # Consider adding some code here to simulate two different policies over the modified MDP
    # and compare the rewards generated by each.
    # BEGIN_YOUR_CODE
    pass
    # END_YOUR_CODE

