# -*- coding: utf-8 -*-
# python 3.7

# A* search

import search_algorithms

def predict(N, weights):
	# Fonction qui donne le trajet réél
	problem = search_algorithms.TransportationProblem(N, weights)
	total_cost, history = search_algorithms.dynamic_programming(problem)
	return [action for action, _, _ in history]


def generate_examples():
	# Simulation d'un réél utilisateur qui a ses préférences
	true_weights = {'walk':1, 'tram':3}
	# C'est ce que l'algorithme d'apprentissage doit deviner
	print(true_weights)
	# génération d'exemples
	return [ (N, predict(N,true_weights)) for N in range(1,50)]

def structured_perceptron(examples):
	weights = {'walk':0, 'tram':0}
	for t in range(100):
		mistakes = 0
		# Itération sur tous les exemples
		for N, true_actions in examples:
			predicted_actions = predict(N, weights)
			if predicted_actions != true_actions:
				mistakes += 1
			for action in true_actions: weights[action] -= 1
			for action in predicted_actions: weights[action] += 1
		print('iteration {}, mistakes {}, weights {}'.format(t, mistakes, weights))
		if mistakes == 0:
			break

examples = generate_examples()

# print('Training Dataset:')
# for example in examples:
# 	print('  {}'.format(example))

structured_perceptron(examples)











