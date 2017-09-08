import random
import operator
import math
import numpy as np



def div(a,b):
    try:
        return a/b
    except Exception:
        return 1


op_dict = {
operator.add : '+',
operator.sub : '-',
operator.mul : 'x',
div : '/'
}



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



class Tree(object):

    def __init__(self, tree):
        self.root = tree


    def eval(self, data_input):
        length = data_input.shape[0]

        f = lambda data : (self.root.eval({'X': x for x in data[:-1]}) - data[-1])**2

        self.error = math.sqrt(sum(map(f, data_input))/length)

        return self.error



def evaluate_population(population, data):
    for individual in population:
        individual.eval(data)



def gen_rnd_expr(func_set, term_set, max_depth, full = False):
    node = None
    length = len(term_set)+len(func_set)
    rand = random.randrange(length)
    print('rand',rand)
    if max_depth == 0 or ((not full) and rand < len(term_set)):
        element = random.choice(term_set)
        print('term', element)

        if element == 'R':
            element = random.randrange(-9,9)

        node = Node(element)
    else:
        func = random.choice(func_set)
        print 'func', func
        child_left = gen_rnd_expr(func_set, term_set, max_depth - 1, full)
        child_right = gen_rnd_expr(func_set, term_set, max_depth - 1, full)

        node = Function_Node(func, child_left, child_right)

    return node



def initialize_population(population_size, max_depth, nodes_func, nodes_term):

    return np.array([Tree(gen_rnd_expr(operators, terminals, max_depth)) for i in range(population_size)])


def get_best_solution(population):
    return min(population, key=(lambda individual : individual.error))



def evaluate_fitness(tree, data_input):
    length = data_input.shape[0]
    # print 'length',length
    # s = 0
    # for data_line in data_input:
    #     d = {'X': x for x in data_line[:-1]}
    #     s +=  (tree.eval(d) - data_line[-1])**2

    f = lambda data : (tree.eval({'X': x for x in data[:-1]}) - data[-1])**2

    return math.sqrt(sum(map(f, data_input))/length)



def level_traverse(queue):
    while queue:
        if queue[0]:
            print(queue[0]),
            queue.append(queue[0].left)
            queue.append(queue[0].right)

        queue = queue[1:]


def in_traverse(node, level = 0):
    if node is None:
        return
    n = str(node) if node.content not in op_dict else op_dict[node.content]
    # print '  ' * level + n
    print '(',n ,
    if node.left is not None:
        in_traverse(node.left, level +1)

    if node.right is not None:
        print ',',
        in_traverse(node.right, level +1)

    print ')',




def genetic_programmin(population_size, nodes_func, nodes_term,
                    p_crossover, p_mutation, p_reproduction, p_alteration):

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
            elif operator == mutation_operator:
                parent1, = select_parents(population, population_size)
                child1 = mutate(parent1)
                children = child1
            elif operator == reproduction_operator:
                parent1, = select_parents(population, population_size)
                child1 = reproduce(parent1)
                children.append(child1)
            elif operator == alteration_operator:
                parent1, = select_parents(population, population_size)
                child1 = alter_architecture(parent1)
                children.append(child1)


        evaluate_population(children)
        s_best = get_best_solution(children, s_best)
        population = children

    return s_best




if __name__ == '__main__':

    random.seed(1)

    data = np.loadtxt('./datasets/keijzer-7-train.csv', delimiter = ',')

    operators = [operator.add, operator.sub, operator.mul]

    terminals = ['X', 'R']
    tree = gen_rnd_expr(operators, terminals, 8)

    in_traverse(tree)
    print

    # print evaluate_fitness(tree,data)

    population = initialize_population(10, 7, operators, terminals)

    # for i in population:
    #     in_traverse(i.root)
    #     print
    #     print evaluate_fitness(i.root, data)
    #     print

    evaluate_population(population, data)

    for i in population:
        # in_traverse(i.root)
        print i.error

    s_best = get_best_solution(population)
    print s_best.error