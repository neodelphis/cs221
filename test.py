def backtraking_search():
	global best_total_cost, b
	best_total_cost = float('inf')  # coût infini au départ

	def recurse():
		global best_total_cost, b
		b =2
		if 3 < best_total_cost:
			best_total_cost = 3
			print('best_total_cost : ', best_total_cost)
			print('b : ', b)
	recurse()

backtraking_search()
