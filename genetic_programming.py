class Node(object):

	def __init__(self, content, left = None, right = None):
		self.left = left
		self.right = right
		self.content = content


	def __str__(self):
		return str(self.content)


	def eval(self, var_map):
		return self.content if self.content not in var_map else var_map[self.content]


class Function_Node(Node):

	def __init__(self, terminal, left, right):
		super(Function_Node, self).__init__(terminal, left, right)


	def eval(self, var_map):
		# return op_dict[self.content](self.left.eval(),self.right.eval())
		return self.content(self.left.eval(var_map),self.right.eval(var_map))



def genetic_programmin(population_size, nodes_func, nodes_term, p_crossover, p_mutation, p_reproduction, p_alteration):

	population = initialize_population(population_size, nodes_func, nodes_term)
	evaluate_population(population)
	s_best = get_best_solution(population)

	while not stop_condition():
		children = []
		while len(children) < population_size:
			operator = select_genetic_operator(p_crossover, p_mutation, p_reproduction, p_alteration)
			if operator == crossover_operator:
				parent1, parent2 = select_parents(population, population_size)
				child1, child2 = crossover(parent1, parent2)
				children.append(child1)
				children.append(child2)
			else if operator == mutation_operator:
				parent1, = select_parents(population, population_size)
				child1 = mutate(parent1)
				children = child1
			else if operator == reproduction_operator:
				parent1, = select_parents(population, population_size)
				child1 = reproduce(parent1)
				children.append(child1)
			else if operator == alteration_operator:
				parent1, = select_parents(population, population_size)
				child1 = alter_architecture(parent1)
				children.append(child1)


		evaluate_population(children)
		s_best = get_best_solution(children, s_best)
		population = children

	return s_best