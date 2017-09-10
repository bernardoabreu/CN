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
    log: 'log',
    math.sin: 'sin',
    math.cos: 'cos'
}

unary = [log, math.cos, math.sin]


class Node(object):
    def __init__(self, content, left=None, right=None):
        self.left = left
        self.right = right
        self.content = content

    def eval(self, var_map):
        return self.content if self.content not in var_map \
            else var_map[self.content]

    def __str__(self):
        return str(self.content)

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

    def get_error(self):
        return self.error

    def __eval(self, data):
        return (self.root.eval({('X' + str(i)): x
                for i, x in enumerate(data[:-1])}) - (data[-1]))**2

    def eval(self, data_input):
        length = data_input.shape[0]

        self.error = math.sqrt(sum(map(self.__eval, data_input)) / length)

        return self.error

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

    def replace_node(self, old_node, new_node):
        if self.root == old_node:
            self.root = new_node
            return True
        else:
            return self.__replace_node(self.root, old_node, new_node)

    def __get_list(self, node, node_list, p_list, p):
        if node is None:
            return

        node_list.append(node)

        if p:
            p_list.append(True if isinstance(node, Function_Node) else False)

        self.__get_list(node.left, node_list, p_list, p)
        self.__get_list(node.right, node_list, p_list, p)

    def get_list(self, p=False):
        node_list = []
        p_list = []

        self.__get_list(self.root, node_list, p_list, p)

        return (node_list, p_list) if p else node_list

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


class Genetic_Programming(object):
    def __init__(self, max_depth, nodes_func, nodes_term, p_crossover,
                 p_mutation, p_reproduction):
        self.max_depth = max_depth
        self.functions = nodes_func
        self.terminals = nodes_term
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.p_reproduction = p_reproduction

        self.initialize_population = self.__ramped_half_and_half
        self.selection = self.__tournament_selection

        self.__full = True
        self.tournament_size = 3

    def set_tournament_size(self, tournament_size):
        self.tournament_size = tournament_size

    def set_probabilities(self, p_crossover, p_mutation, p_reproduction):
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.p_reproduction = p_reproduction

    def set_initialization(self, init_type):
        if init_type == 'half and half':
            self.initialize_population = self.__ramped_half_and_half
        elif init_type == 'grow':
            self.initialize_population = self.__simple_initialization
            self.__full = False
        elif init_type == 'full':
            self.initialize_population = self.__simple_initialization
            self.__full = True

    def __ramped_half_and_half(self, population_size, max_depth, funcs, terms):
        pop = []
        group = (population_size / (max_depth - 1))
        full = True

        for i in range(2, max_depth + 1):
            for j in range(group):
                pop.append(Tree(self.__gen_rnd_expr(funcs, terms, i, full)))
                full = not full

        if pop < population_size:
            pop.append(Tree(self.__gen_rnd_expr(funcs, terms, i, full)))

        return pop

    def __simple_initialization(self, pop_size, max_depth, funcs, terms):
        return [Tree(self.__gen_rnd_expr(funcs, terms, max_depth, self.__full))
                for i in range(pop_size)]

    def set_selection(self, selection_type):
        if selection_type == 'tournament':
            self.selection = self.__tournament_selection

    def __get_best_solution(self, population):
        return min(population, key=(lambda individual: individual.error))

    def __tournament_selection(self, population):
        sample = random.sample(population, self.tournament_size)
        return self.__get_best_solution(sample)

    def __gen_rnd_function(self, func, func_set, term_set, max_depth):
        child_left = self.__gen_rnd_expr(func_set, term_set, max_depth - 1)
        child_right = None if func in unary else \
            self.__gen_rnd_expr(func_set, term_set, max_depth - 1)

        return Function_Node(func, child_left, child_right)

    def __gen_rnd_expr(self, func_set, term_set, max_depth, full=False):
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
            func = random.choice(func_set)
            # func = func_set[rand - len(term_set)]
            # print 'func', func

            node = self.__gen_rnd_function(func, func_set, term_set, max_depth)

        return node

    def __select_genetic_operator(self):
        return np.random.choice(['crossover', 'mutation', 'reproduction'],
                                p=[self.p_crossover, self.p_mutation,
                                   self.p_reproduction])

    def evaluate_population(self, population, data):
        for individual in population:
            individual.eval(data)

    def crossover(self, parent1, parent2):
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        list1 = child1.get_list()
        list2 = child2.get_list()

        element1 = random.choice(list1)
        element2 = random.choice(list2)

        child1.replace_node(element1, element2)
        child2.replace_node(element2, element1)

        return child1, child2

    def mutation(self, parent):
        mutant = copy.deepcopy(parent)
        mutant_list = mutant.get_list()

        element = random.choice(mutant_list)

        is_function = isinstance(element, Function_Node)

        length = len(self.terminals) + len(self.functions)
        rand = random.randrange(length)

        if rand < len(self.terminals):
            term = self.terminals[rand]

            if term == 'R':
                term = random.randrange(-5, 5)

            # print('term', term)
            if is_function:
                # print 'Replace function with terminal'
                node = Node(term)
                mutant.replace_node(element, node)
            else:
                # print 'Replace terminal'
                element.content = term
        else:
            func = self.functions[rand - len(self.terminals)]
            # print 'func', func

            depth = max(2, self.max_depth / 2)

            if is_function:
                # print 'Replace terminal'
                if func in unary:
                    if element.right is not None:
                        element.right = None
                elif element.right is None:
                    element.right = self.__gen_rnd_function(func,
                                                            self.functions,
                                                            self.terminals,
                                                            depth)
                element.content = func
            else:
                # print 'Replace terminal with function'
                node = self.__gen_rnd_function(func, self.functions,
                                               self.terminals, depth)
                mutant.replace_node(element, node)

        return mutant

    def reproduction(self, parent):
        return copy.deepcopy(parent)

    def run(self, data, population_size, generations, elitism=0):

        population = self.initialize_population(population_size,
                                                self.max_depth,
                                                self.functions, self.terminals)
        self.evaluate_population(population, data)
        population.sort(key=lambda x: x.error)
        # s_best = get_best_solution(population)
        s_best = population[0]
        for p in population:
            p.print_tree()

        # print 'initial population:'
        # print map(lambda x: x.error, population)

        current_generation = 0

        while current_generation < generations and s_best.get_error() > 0.0:
            children = []
            print('generation: ' + str(current_generation) + ' best:' +
                  str(s_best.get_error()))
            # print map(lambda x: x.error, population),

            if elitism:
                children = population[:elitism]

            while len(children) < population_size:
                operator = self.__select_genetic_operator()
                # print operator
                parent1 = self.selection(population)
                if operator == 'crossover':
                    parent2 = self.selection(population)
                    child1, child2 = self.crossover(parent1, parent2)
                    children.append(child1)
                    children.append(child2)
                elif operator == 'mutation':
                    child1 = self.mutation(parent1)
                    children.append(child1)
                elif operator == 'reproduction':
                    child1 = self.reproduction(parent1)
                    children.append(child1)

            self.evaluate_population(children, data)
            population = sorted(children,
                                key=lambda x: x.error)[:population_size]
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

    train_data = np.loadtxt('./datasets/keijzer-7-train.csv', delimiter=',')

    population_size = 100
    max_depth = 7
    generations = 100
    tournament_size = 10
    functions = [operator.add, operator.sub, operator.mul, div, math.sin,
                 math.cos, log]
    terminals = ['R'] + ['X' + str(i) for i in range(train_data.shape[1] - 1)]
    print terminals
    p_crossover = 0.9
    p_mutation = 0.1
    p_reproduction = 0.0
    elitism = 5

    gp = Genetic_Programming(max_depth, functions, terminals, p_crossover,
                             p_mutation, p_reproduction)

    gp.set_tournament_size(tournament_size)

    best = gp.run(train_data, population_size, generations, elitism)

    print best.get_error()
    best.print_tree()

    test_data = np.loadtxt('./datasets/keijzer-7-test.csv', delimiter=',')

    best.eval(test_data)
    print best.get_error()
