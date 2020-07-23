# -*- coding: utf-8 -*-
from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def __init__(self):
        self.lastPositions = []
        self.dc = None

    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
        ------------------------------------------------------------------------------
        Description of GameState and helper functions:

        A GameState specifies the full game state, including the food, capsules,
        agent configurations and score changes. In this function, the |gameState| argument
        is an object of GameState class. Following are a few of the helper methods that you
        can use to query a GameState object to gather information about the present state
        of Pac-Man, the ghosts and the maze.

        gameState.getLegalActions():
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor state after the specified agent takes the action.
        Pac-Man is always agent 0.

        gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

        gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.getScore():
        Returns the score corresponding to the current state of the game


        The GameState class is defined in pacman.py and you might want to look into that for
        other helper methods, though you don't need to.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (problem 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction. Terminal states can be found by one of the following:
        pacman won, pacman lost or there are no legal moves.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        Directions.STOP:
        The stop direction, which is always legal

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.getScore():
        Returns the score corresponding to the current state of the game

        gameState.isWin():
        Returns True if it's a winning state

        gameState.isLose():
        Returns True if it's a losing state

        self.depth:
        The depth to which search should continue

        """

        # BEGIN_YOUR_CODE (our solution is 26 lines of code, but don't worry if you deviate from this)

        def recurse(gameState, agentIndex, currentDepth):
            """
            Renvoie un tuple (utility, action)
            Doit être valable quelque soit le type d'agent
            """
            # Nombre total d'agents dans le jeu
            numAgents = gameState.getNumAgents()

            # Liste des actions possibles pour un agent
            # agentIndex=0 : Pacman, ghosts : >= 1
            legalMoves = gameState.getLegalActions(agentIndex)

            # Cas des feuilles ultimes de notre arbre de décision
            if gameState.isWin():
                return (gameState.getScore(), None)
            if gameState.isLose():
                return (gameState.getScore(), None)
            if legalMoves is None:
                # Cas où il n'y a plus de mouvement possible
                return (gameState.getScore(), None)

            # Cas des "feuilles" atteintes à d_max, profondeur maximale à laquelle on fait la recherche
            # Ici on fait appel à notre fonction d'évaluation de la situation
            # Toujours évaluée du point de vue de pacman
            if currentDepth == 0:
                # Choose one of the best actions
                scores = [self.evaluationFunction(gameState) for action in legalMoves]
                bestScore = max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
                return (bestScore, legalMoves[chosenIndex])

            # Cas principal où l'on reste dans la boucle de récurrence
            # Choix du max ou du min selon pacman/ghost dans
            # une liste des candidats : [(utilité du successeur, action qui mène à ce successeur)]
            if agentIndex == 0:  # Pacman
                candidates = []
                for action in legalMoves:
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    utility_succ, _ = recurse(nextGameState, agentIndex + 1, currentDepth)
                    candidates.append((utility_succ, action))
                # En fait l'utilité maximale du successeur remonte d'un niveau
                # car il n'y a pas de modification de l'utilité dans ce modèle
                return max(candidates)  # max sur un tuple <=> max sur la première valeur ici utilité
            else:  # Cas des fantômes
                # Gestion des joueurs et de la profondeur de recherche
                if agentIndex == numAgents - 1:  # Dernier fantôme à considérer
                    nextAgentIndex = 0  # On repasse à Pacman
                    currentDepth -= 1
                else:  # Tous les autres fantômes
                    nextAgentIndex = agentIndex + 1

                candidates = []
                for action in legalMoves:
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    utility_succ, _ = recurse(nextGameState, nextAgentIndex, currentDepth)
                    candidates.append((utility_succ, action))
                return min(candidates)

            # elif agentIndex == numAgents - 1:  # Dernier fantôme à considérer
            #     candidates = []
            #     for action in legalMoves:
            #         nextGameState = gameState.generateSuccessor(agentIndex, action)
            #         utility_succ, _ = recurse(nextGameState, 0, currentDepth - 1)  # On repasse à Pacman
            #         candidates.append((utility_succ, action))
            #     return min(candidates)
            # else:  # Tous les autres fantômes
            #     candidates = []
            #     for action in legalMoves:
            #         nextGameState = gameState.generateSuccessor(agentIndex, action)
            #         utility_succ, _ = recurse(nextGameState, agentIndex + 1, currentDepth)
            #         candidates.append((utility_succ, action))
            #     return min(candidates)

        # Code de la méthode getAction
        # Profondeur de la recherche en cours
        currentDepth = self.depth

        # Cette fonction sera appelée pour pacman seulement
        agentIndex = 0

        utility, action = recurse(gameState, agentIndex, currentDepth)
        # print 'utility : ', utility

        return action
    # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (problem 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        Inspiration pour l'algorithme:
        https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        """

        # BEGIN_YOUR_CODE (our solution is 49 lines of code, but don't worry if you deviate from this)

        def max_value(gameState, agentIndex, currentDepth, alpha, beta):
            """
            Renvoie un tuple (utility, action)
            utilisé seulement pour les noeuds max, soit ici pacman agentIndex=0
            """
            # Nombre total d'agents dans le jeu
            numAgents = gameState.getNumAgents()

            # List of legal actions for an agent
            legalMoves = gameState.getLegalActions(agentIndex)

            # Cas des feuilles ultimes de notre arbre de décision
            if gameState.isWin():
                return (gameState.getScore(), None)
            if gameState.isLose():
                return (gameState.getScore(), None)
            if legalMoves is None:
                # Cas où il n'y a plus de mouvement possible
                return (gameState.getScore(), None)

            # Cas des "feuilles" atteintes à d_max, profondeur maximale à laquelle on fait la recherche
            # Ici on fait appel à notre fonction d'évaluation de la situation
            # Toujours évaluée du point de vue de pacman
            if currentDepth == 0:
                # Choose one of the best actions
                scores = [self.evaluationFunction(gameState) for action in legalMoves]
                bestScore = max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
                # print currentDepth, bestScore, legalMoves[chosenIndex]
                return (bestScore, legalMoves[chosenIndex])

            # Cas principal où l'on reste dans les boucles de récurrence
            best_value = -float('inf')
            # best_value = gameState.getScore()
            # print 'score: ', best_value
            best_action = None
            assert agentIndex == 0  # On s'assure qu'on travaille bien avec Pacman

            for action in legalMoves:
                nextGameState = gameState.generateSuccessor(agentIndex, action)
                value, _ = min_value(nextGameState, agentIndex + 1, currentDepth, alpha, beta)
                best_value, best_action = max((best_value, best_action), (value, action))
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            # print currentDepth, action, agentIndex, best_value, best_action
            return best_value, best_action

        def min_value(gameState, agentIndex, currentDepth, alpha, beta):
            """
            Renvoie un tuple (utility, action)
            utilisé seulement pour les noeuds min, soit ici ghost 0 < agentIndex < NumAgents
            """

            # On s'assure que l'on travaille bien avec les fantômes
            assert agentIndex > 0
            assert agentIndex < gameState.getNumAgents()

            # Nombre total d'agents dans le jeu
            numAgents = gameState.getNumAgents()
            # print 'numAgents =', numAgents

            # List of legal actions for an agent
            legalMoves = gameState.getLegalActions(agentIndex)
            # print 'agentIndex, legalMoves'
            # print agentIndex, legalMoves
            # Cas des feuilles ultimes de notre arbre de décision
            if gameState.isWin():
                return (gameState.getScore(), None)
            if gameState.isLose():
                return (gameState.getScore(), None)
            if legalMoves is None:
                # Cas où il n'y a plus de mouvement possible
                return (gameState.getScore(), None)

            if agentIndex == numAgents - 1:  # Dernier fantôme à considérer
                best_value = float('inf')
                # best_value = gameState.getScore()
                best_action = None
                for action in legalMoves:
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    value, _ = max_value(nextGameState, 0, currentDepth - 1, alpha, beta)   # On repasse à Pacman
                    best_value, best_action = min((best_value, best_action), (value, action))
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
                # print '>> ', currentDepth, agentIndex, best_value, best_action
                return best_value, best_action

            else:  # Un des fantômes, mais pas le dernier
                best_value = float('inf')
                # best_value = gameState.getScore()
                best_action = None
                for action in legalMoves:
                    nextGameState = gameState.generateSuccessor(agentIndex, action)
                    value, _ = min_value(nextGameState, agentIndex + 1, currentDepth, alpha, beta)   # prochain fantôme
                    best_value, best_action = min((best_value, best_action), (value, action))
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
                # print '>> ', agentIndex, best_value, best_action
                return best_value, best_action

        # Profondeur de la recherche en cours
        currentDepth = self.depth

        # Cette fonction sera appelée pour pacman seulement
        agentIndex = 0
        alpha = -float('inf')
        beta = float('inf')

        utility, action = max_value(gameState, agentIndex, currentDepth, alpha, beta)
        # print 'utility, action : ', utility, action

        return action

        # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (problem 3)
    """


def getAction(self, gameState):
    """
    Returns the expectimax action using self.depth and self.evaluationFunction

    All ghosts should be modeled as choosing uniformly at random from their
    legal moves.
    """

    # BEGIN_YOUR_CODE (our solution is 25 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function


def betterEvaluationFunction(currentGameState):
    """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
    """

    # BEGIN_YOUR_CODE (our solution is 26 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

    # Abbreviation
    better = betterEvaluationFunction
