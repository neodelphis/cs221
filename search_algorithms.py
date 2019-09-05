# -*- coding: utf-8 -*-
# python 3.7
import sys
from Queue import PriorityQueue
# from queue import PriorityQueue
# étrange sur le portable avec la même version de python il faut un q minuscule à queue
# comme si on était en 2.*


sys.setrecursionlimit(10000)


class TransportationProblem(object):
	"""
	Problème d'un déplacement de 1 jusqu'à N
	2 options à chaque étape s:
	walk: coût 1, avance à s+1
	tram: coût 2, avance à 2s 
	"""

	def __init__(self, N, weights = {'walk':0, 'tram':0}):
		self.N = N
		self.weights = weights

	def start_state(self):
		return 1

	def is_end(self, state):
		return state == self.N

	def action_successor_cost(self, state):
		"""
		output:
			une liste de (action, new_state, cost)
		"""
		successor = []
		if state+1 <= self.N:
			successor.append(('walk', state+1, self.weights['walk']))
		if 2*state <= self.N:
			successor.append(('tram', 2*state, self.weights['tram']))
		return successor


def backtraking_search(problem):
	global best_total_cost , best_history  # variables globales
	best_total_cost = float('inf')  # coût infini au départ
	best_history = []

	def recurse(state, history, total_cost):
		global best_total_cost , best_history
		# Nécessité de placer les variables globales à tous les niveaux pour les fonctions imbriquées
		if problem.is_end(state):
			if total_cost < best_total_cost :
				best_total_cost = total_cost
				best_history = history
			return
		for action, new_state, cost in problem.action_successor_cost(state):
			# history += [(action, new_state, cost)] # => garde en mémoire toutes les options explorées
			# total_cost += cost # => plante si on fait ça, pourquoi?
			recurse(new_state, history + [(action, new_state, cost)], total_cost + cost)

	# Initialisation de la récursivité
	recurse(problem.start_state(), history=[], total_cost=0)

	# Une fois l'exploration récursive effectuée
	return best_total_cost, best_history


def dynamic_programming(problem):
	cache = {}  # state => future_cost(state), action, new_state, cost

	def future_cost(state):
		if problem.is_end(state):
			return 0

		if state in cache:
			return cache[state][0]  # future_cost(state)

		# On veut connaître l'action avec le coût minimum
		# result = (total_cost, action, new_state, cost)  # Nom de variable peu clair
		best_result = (float('inf'), None, None, None)
		for action, new_state, cost in problem.action_successor_cost(state):
			total_cost = cost + future_cost(new_state)  # Coût total à partir de cet étape s pour cette action
			result = (total_cost, action, new_state, cost)
			best_result = min(result, best_result)  # teste sur la première valeur du tuple

		cache[state] = best_result
		return best_result[0] # Coût total minimum trouvé pour l'instant à partir de cet étape s


	# Initialisation du problème
	state = problem.start_state()
	best_total_cost = future_cost(state)

	# Reconstruction de l'historique de la solution trouvée
	history = []
	while not problem.is_end(state):
		_, action, new_state, cost = cache[state]
		history.append((action, new_state, cost))
		state = new_state

	# Solution
	return best_total_cost, history


def uniform_cost_search(problem):
	# A la frontière on stocke le noeud (state) et le coût pour y arriver
	# PriorityQueue element : (priority_number, data), ici (path_cost, state, history)
	# (cost of reaching state, current state, history of states visited)
	# history of states visited = [(action, new_state, cost)]
	frontier = PriorityQueue()

	# Initialisation de la frontière
	history = []
	frontier.put( (0, problem.start_state(), history) ) 

	while True:
		# On récupère un noeud avec le plus faible coût jusqu'à maintenant
		path_cost, state, history = frontier.get()
		
		if problem.is_end(state):
			return (path_cost, history)

		for action, new_state, cost in problem.action_successor_cost(state):
			# On met les prochains noeuds avec leur coût et le trajet dans la PriorityQueue
			# Celui avec le plus faible noeud est présenté en premier
			frontier.put( ( path_cost + cost, new_state, history + [(action, new_state, cost)]) ) 



def print_solution(solution):
	best_total_cost, best_history = solution
	print('best_total_cost : ', best_total_cost)
	for item in best_history:
		print(item)	


# # Appel à notre fonction
# problem = TransportationProblem(300)



# from timeit import default_timer as timer

# start = timer()
# print('backtraking_search')
# solution = backtraking_search(problem)
# print_solution(solution)
# end = timer()
# print(end - start) # Time in seconds, e.g. 5.38091952400282

# start = timer()
# print('dynamic_programming')
# solution = dynamic_programming(problem)
# print_solution(solution)
# end = timer()
# print(end - start)

# start = timer()
# print('uniform_cost_search')
# solution = uniform_cost_search(problem)
# print_solution(solution)
# end = timer()
# print(end - start)

































