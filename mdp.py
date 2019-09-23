# -*- coding: utf-8 -*- 
# python 3.7

# Markov Decision Process


# Modélisation du problème
# ------------------------
# 
# Problème d'un déplacement de 1 jusqu'à N
# 2 options à chaque étape s:
# walk: coût 1, avance à s+1
# tram: coût 2, avance à 2s avec un risque d'échec de x% (il reste sur place)

class TransportationMDP:
	walk_cost = 1
	tram_cost = 2
	fail_prob  = 0.5  # Failure probability


	def __init__(self, N):
		self.N = N
 
	def start_state(self):
		return 1

	def is_end(self, state):
		return state == self.N

	def actions(self, state):
		"""
		Ensemble des actions possibles pour un état donné
		"""
		results = []
		if state + 1 <= self.N:
			results.append('walk')
		if state * 2 <= self.N:
			results.append('tram')
		return results

	def transitions(self, state, action):
		"""
		Renvoie une liste de (new_state, probability, reward) où
		new_state   : s', état dans lequel on peut arriver
		probability : T(s,a,s')
		reward      : Reward(s,a,s')
		"""
		results = []
		if action == 'walk':
			results.append((state+1, 1, -self.walk_cost))
		elif action == 'tram':
			results.append((2*state, 1-self.fail_prob, -self.tram_cost))
			results.append((state, self.fail_prob, -self.tram_cost))
		return results

	def discount(self):
		return 1

	def states(self):
		return range(1, self.N +1)



# Algorihtme de déduction (inference algorithm)
# ---------------------------------------------

def value_iteration(mdp):
	# On veut calculer une estimation de V_opt(state)
	# Fonction V : state -> estimate of V_opt(state)
	# Value V
	V = {}

	# Policy pi
	# Fonction pi: state -> estimate of pi_opt(state)
	pi = {}

	# A partir de l'estimation courante de V
	# new_state : s'
	def Q(state, action):
		return sum(
				   probability * (reward + mdp.discount() * V[new_state])
				   for new_state, probability, reward in mdp.transitions(state, action)
				  )

	# Initialisation
	for state in mdp.states():
		V[state] = 0

	# Itérations
	while True:
		newV = {} # nouvelles valeurs à l'itération t basé sur V de t-1

		# Calcul du nouveau V
		for state in mdp.states():
			if mdp.is_end(state):
				newV[state], pi[state] = 0, None
			else:
				newV[state], pi[state] = max( (Q(state, action), action) for action in mdp.actions(state))
				# le max sur un tuple se fait d'abord sur la première valeur
				# et en cas d'égalité sur la seconde (ici un ordre alphabétique)
			print('{}: {} {}'.format(state, newV[state], pi[state]))

		# Test de convergence
		if max( abs(newV[state] - V[state]) for state in mdp.states() ) < 1e-10:
			break

		V = newV



# Main
# ----
mdp = TransportationMDP(N=20)
# print(mdp.transitions(3, 'tram'))

value_iteration(mdp)





