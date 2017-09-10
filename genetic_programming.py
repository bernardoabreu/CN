import random
import operator
import math
import numpy as np
import copy


def div(a, b):
    return 1 if b == 0 else a / b


def log(x):
    try:
        return math.log(x)
    except ValueError:
        return 0


op_dict = {
    operator.add: '+',
    operator.sub: '-',
    operator.mul: 'x',
    div: '/',
    log: 'log'
}

unary = [log]


class Node(object):
    def __init__(self, content, left=None, right=None):
        self.left = left
        self.right = right
        self.content = content

    def __str__(self):
        return str(self.content)

    def eval(self, var_map):
        return self.content if self.content not in var_map \
            else var_map[self.content]

    def print_tree(self):
        self.__print(self)
        print

    def __print(self, node, level=0):
        if node is None:
            return
        n = str(node) if node.content not in op_dict else op_dict[node.content]
        # print '  ' * level + n

        print '(', n,

        if node.left is not None:
            self.__print(node.left, level + 1)

        if node.right is not None:
            print ',',
            self.__print(node.right, level + 1)

        print ')',


class Function_Node(Node):

    def __init__(self, terminal, left, right):
        super(Function_Node, self).__init__(terminal, left, right)

    def eval(self, var_map):
        # return op_dict[self.content](self.left.eval(),self.right.eval())
        left_eval = self.left.eval(var_map)

        return self.content(left_eval) if self.right is None else \
            self.content(left_eval, self.right.eval(var_map))


class Tree(object):
    def __init__(self, tree):
        self.root = tree
        self.error = None

    def __eval(self, data):
        return (self.root.eval({('X' + str(i)): x
                for i, x in enumerate(data[:-1])}) - (data[-1]))**2

    def eval(self, data_input):
        length = data_input.shape[0]

        self.error = math.sqrt(sum(map(self.__eval, data_input)) / length)

        return self.error

    def print_tree(self):
        self.__print(self.root)
        print

    def __print(self, node, level=0):
        if node is None:
            return
        n = str(node) if node.content not in op_dict else op_dict[node.content]
        # print '  ' * level + n
        print '(', n,
        if node.left is not None:
            self.__print(node.left, level + 1)

        if node.right is not None:
            print ',',
            self.__print(node.right, level + 1)

        print ')',

    # def get_size(self, node):
    #     if node is None:
    #         return 0

    #     return 1 + self.get_size(node.left) + self.get_size(node.right)

    def replace_node(self, old_node, new_node):
        if self.root == old_node:
            self.root = new_node
            return True
        else:
            return self.__replace_node(self.root, old_node, new_node)

    def __replace_node(self, node, old_node, new_node):
        if node is None:
            return False

        if node.left == old_node:
            node.left = new_node
            return True

        if node.right == old_node:
            node.right = new_node
            return True

        return self.__replace_node(node.left, old_node, new_node) or \
            self.__replace_node(node.right, old_node, new_node)

    def get_list(self, p=None):
        node_list = []
        p_list = []

        self.__get_list(self.root, node_list, p_list, p)

        return (node_list, p_list) if p is not None else node_list

    def __get_list(self, node, node_list, p_list, p):
        if node is None:
            return

        node_list.append(node)

        if p is not None:
            p_list.append(p[1] if isinstance(node, Function_Node) else p[0])

        self.__get_list(node.left, node_list, p_list, p)
        self.__get_list(node.right, node_list, p_list, p)


def evaluate_population(population, data):
    for individual in population:
        individual.eval(data)


def gen_rnd_function(func, func_set, term_set, max_depth):
    child_left = gen_rnd_expr(func_set, term_set, max_depth - 1)
    child_right = None if func in unary else \
        gen_rnd_expr(func_set, term_set, max_depth - 1)

    return Function_Node(func, child_left, child_right)


def gen_rnd_expr(func_set, term_set, max_depth, full=False):
    node = None
    length = len(term_set) + len(func_set)
    rand = random.randrange(length)
    # print('rand', rand)
    if max_depth == 0 or ((not full) and rand < len(term_set)):
        term = random.choice(term_set)
        # term = term_set[rand]
        # print('term', element)

        if term == 'R':
            term = random.randrange(-9, 9)

        node = Node(term)
    else:
        # func = random.choice(func_set)
        func = func_set[rand - len(term_set)]
        # print 'func', func
        # child_left = gen_rnd_expr(func_set, term_set, max_depth - 1, full)
        # child_right = gen_rnd_expr(func_set, term_set, max_depth - 1, full)

        # node = Function_Node(func, child_left, child_right)
        node = gen_rnd_function(func, func_set, term_set, max_depth)

    return node


def initialize_population(population_size, max_depth,
                          nodes_func, nodes_term, full=False):
    return [Tree(gen_rnd_expr(nodes_func, nodes_term, max_depth, full))
            for i in range(population_size)]


def get_best_solution(population):
    return min(population, key=(lambda individual: individual.error))


def tournament_selection(population, tournament_size):
    sample = random.sample(population, tournament_size)
    return copy.deepcopy(get_best_solution(sample))


def select_genetic_operator(p_crossover, p_mutation, p_reproduction):
    return np.random.choice(['crossover', 'mutation', 'reproduction'],
                            p=[p_crossover, p_mutation, p_reproduction])


def crossover(parent1, parent2):
    list1 = parent1.get_list()
    list2 = parent2.get_list()

    element1 = np.random.choice(list1)
    element2 = np.random.choice(list2)

    # print 'element1',
    # element1.print_tree()
    # print 'element2',
    # element2.print_tree()
    parent1.replace_node(element1, element2)
    parent2.replace_node(element2, element1)

    return parent1, parent2


def mutation(parent1, func_set, term_set, max_depth):
    # parent1.print_tree()
    list1 = parent1.get_list()

    element1 = np.random.choice(list1)
    # c = copy.deepcopy(parent1)
    # print 'element1', str(element1)
    is_function = isinstance(element1, Function_Node)

    length = len(term_set) + len(func_set)
    rand = random.randrange(length)
    # print('rand', rand)
    # print 'parent1',
    # parent1.print_tree()
    # print 'element1',
    # element1.print_tree()

    if rand < len(term_set):
        # term = random.choice(term_set)
        term = term_set[rand]

        if term == 'R':
            term = random.randrange(-5, 5)

        # print('term', term)
        if is_function:
            # print 'Replace function with terminal'
            node = Node(term)
            parent1.replace_node(element1, node)
        else:
            # print 'Replace terminal'
            element1.content = term
    else:
        # func = random.choice(func_set)
        func = func_set[rand - len(term_set)]
        # print 'func', func

        if is_function:
            # print 'Replace terminal'
            if func in unary:
                if element1.right is not None:
                    element1.right = None
            elif element1.right is None:
                element1.right = gen_rnd_function(func, func_set, term_set,
                                                  max_depth)
            element1.content = func
        else:
            # print 'Replace terminal with function'
            # child_left = gen_rnd_expr(func_set, term_set, max_depth - 1)
            # child_right = gen_rnd_expr(func_set, term_set, max_depth - 1)
            # node = Function_Node(func, child_left, child_right)
            node = gen_rnd_function(func, func_set, term_set, max_depth)
            parent1.replace_node(element1, node)

    # print 'parent1',
    # parent1.print_tree()
    return parent1


def genetic_programming(data, population_size, individual_depth, generations,
                        tournament_size, nodes_func, nodes_term,
                        p_crossover, p_mutation, p_reproduction, elitism=0):

    population = initialize_population(
        population_size, individual_depth, nodes_func, nodes_term)
    evaluate_population(population, data)
    population.sort(key=lambda x: x.error)
    # s_best = get_best_solution(population)
    s_best = population[0]
    # for p in population:
    #     p.print_tree()

    # print 'initial population:'
    # print map(lambda x: x.error, population)

    current_generation = 0

    while current_generation < generations and s_best.error > 0.0:
        children = []
        print 'generation:', current_generation, 'best:', s_best.error
        # print map(lambda x: x.error, population),

        if elitism:
            children = population[:elitism]

        while len(children) < population_size:
            operator = select_genetic_operator(p_crossover, p_mutation,
                                               p_reproduction)
            # print operator
            parent1 = tournament_selection(population, tournament_size)
            if operator == 'crossover':
                parent2 = tournament_selection(population, tournament_size)
                child1, child2 = crossover(parent1, parent2)
                children.append(child1)
                children.append(child2)
            elif operator == 'mutation':
                # print 'mutation'
                child1 = mutation(parent1, nodes_func, nodes_term, max_depth)
                children.append(child1)
            elif operator == 'reproduction':
                children.append(parent1)
            # elif operator == alteration_operator:
            #     parent1, = select_parents(population, population_size)
            #     child1 = alter_architecture(parent1)
            #     children.append(child1)

        evaluate_population(children, data)
        population = sorted(children, key=lambda x: x.error)[:population_size]
        # s_best = get_best_solution(population)
        s_best = population[0]

        current_generation += 1

    return s_best


def eeval(data_input):
    length = data_input.shape[0]

    def e(data):
        return (log(data[0]) - (data[-1]))**2

    return math.sqrt(sum(map(e, data_input)) / length)


if __name__ == '__main__':
    seed = None
    random.seed(seed)
    np.random.seed(seed)
    max_depth = 3

    data = np.loadtxt('./datasets/keijzer-7-test.csv', delimiter=',')

    population_size = 50
    individual_depth = 3
    generations = 50
    tournament_size = 5
    nodes_func = [operator.add, operator.sub, operator.mul, div, log]
    nodes_term = ['R'] + ['X' + str(i) for i in range(data.shape[1] - 1)]
    p_crossover = 0.9
    p_mutation = 0.1
    p_reproduction = 0.0
    elitism = 1

    # print log in unary
    best = genetic_programming(data, population_size, individual_depth,
                               generations, tournament_size, nodes_func,
                               nodes_term, p_crossover, p_mutation,
                               p_reproduction, elitism)

    print best.error
    best.print_tree()

    # operators = [operator.add, operator.sub, operator.mul]

    # terminals = ['X', 'R']

    # population = initialize_population(
    #     10, max_depth, operators, terminals, full=True)
    # population.sort(key=lambda x: x.error)
    # # for i in population:
    # #     in_traverse(i.root)
    # #     print
    # #     print evaluate_fitness(i.root, data)
    # #     print

    # evaluate_population(population, data)

    # for i in population:
    #     i.print_tree()

    # parent1 = tournament_selection(population, 3)
    # parent2 = tournament_selection(population, 3)

    # print 'parent1',
    # parent1.print_tree()

    # child1 = mutation(parent1, operators, terminals, max_depth)

    # print 'child1',
    # child1.print_tree()

    # for i in population:
    #     i.print_tree()

    # population1 = sorted(population, key=lambda x: x.error)

    # for i, j in zip(population, population1):
    #     print i.error, j.error
    # print 'parent2',
    # parent2.print_tree()

    # child1, child2 = crossover(parent1, parent2)

    # print 'child1',
    # child1.print_tree()
    # print 'child2',
    # child2.print_tree()

    # for i in population:
    #     i.print_tree()

    # for i in population:
    #     # in_traverse(i.root)
    #     print i.error

    # s_best = get_best_solution(population)

    # s_best.print_tree()
    # print  map(str, s_best.get_list())

    # print s_best.error

    # print
    # for i in range(5):
    #     ss = tournament_selection(population,10)
    #     ss.print_tree()
    #     print  map(str, ss.get_list())
    #     print ss.error