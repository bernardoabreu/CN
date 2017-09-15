#!/usr/bin/env python

import random
import copy
from individual import Individual

from functions import *

from node import Function_Node
from node import Terminal_Node


def mean(x):
    return sum(x) / len(x)


def ramped_half_and_half(population_size, max_depth, funcs, terms):
    pop = []
    group = (population_size / (max_depth - 1))
    full = True

    for i in range(2, max_depth + 1):
        for j in range(group):
            pop.append(Individual(gen_rnd_expr(funcs, terms, i, full)))
            full = not full

    if pop < population_size:
        pop.append(Individual(gen_rnd_expr(funcs, terms, i, full)))

    return pop


def simple_initialization(pop_size, max_depth, funcs, terms, full):
    return [Individual(gen_rnd_expr(funcs, terms, max_depth, full))
            for i in range(pop_size)]


def get_best_solution(population):
    return min(population, key=(lambda individual: individual.error))


def tournament_selection(population):
    sample = random.sample(population, self.tournament_size)
    return get_best_solution(sample)


def gen_rnd_function(func, func_set, term_set, max_depth):
    child_left = gen_rnd_expr(func_set, term_set, max_depth - 1)
    child_right = None if func in UNARY else \
        gen_rnd_expr(func_set, term_set, max_depth - 1)

    return Function_Node(func, child_left, child_right)


def gen_rnd_expr(func_set, term_set, max_depth, full=False):
    node = None
    length = len(term_set) + len(func_set)
    rand = random.randrange(length)
    print('rand', rand)
    print 'max_depth', max_depth
    if max_depth == 0 or ((not full) and rand < len(term_set)):
        term = random.choice(term_set)
        # term = term_set[rand]
        print('term', term)

        if term == 'R':
            term = random.choice(
                [n for n in range(-5, 6) if n])

        node = Terminal_Node(term)
    else:
        func = random.choice(func_set)
        # func = func_set[rand - len(term_set)]
        print 'func', func

        node = gen_rnd_function(func, func_set, term_set, max_depth)

    return node


def select_genetic_operator(self, p_crossover, p_mutation):
    p = random.random()

    if p > crossover + p_mutation:
        return 'reproduction'
    else:
        return 'mutation' if p > crossover else 'crossover'


def evaluate_population(population, data):
    for individual in population:
        individual.eval(data)


def crossover(parent1, parent2):
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)
    list1 = child1.get_list()
    list2 = child2.get_list()

    element1 = random.choice(list1)
    element2 = random.choice(list2)

    child1.replace_node(element1, element2)
    child2.replace_node(element2, element1)

    return child1, child2


def mutation(parent, terminals, functions):
    mutant = copy.deepcopy(parent)
    mutant_list = mutant.get_list()

    element = random.choice(mutant_list)
    content = element.get_content()
    element_right = element.get_right_child()

    print 'Replace', content
    is_function = isinstance(element, Function_Node)
    new_terminals = [i for i in terminals if i != content]
    new_functions = [i for i in functions if i != content]

    length = len(new_terminals) + len(new_functions)
    rand = random.randrange(length)

    if rand < len(new_terminals):
        term = new_terminals[rand]

        if term == 'R':
            term = random.choice(
                [n for n in range(-5, 6) if n != content])

        print('term', term)
        if is_function:
            print 'Replace function with terminal'
            node = Terminal_Node(term)
            mutant.replace_node(element, node)
        else:
            print 'Replace terminal'
            element.content = term
    else:
        func = new_functions[rand - len(new_terminals)]
        print 'func', func

        # depth = max(2, self.max_depth / 2)
        depth = 2

        if is_function:
            print 'Replace terminal'
            if func in UNARY:
                if element_right is not None:
                    element.set_right_child(None)
            elif element_right is None:
                element.set_right_child(gen_rnd_function(func, functions,
                                        terminals, depth))
            element.content = func
        else:
            print 'Replace terminal with function'
            node = gen_rnd_function(func, functions, terminals, depth)
            mutant.replace_node(element, node)

    return mutant


def reproduction(parent):
    return copy.deepcopy(parent)


def run(data, max_depth, functions, terminals, population_size,
        generations, elitism=0):

    population = initialize_population(population_size, max_depth,
                                       functions, terminals)
    evaluate_population(population, data)
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
        print('Generation: ' + str(current_generation) + ' Best:' +
              str(s_best.get_error()) + ' Mean:' +
              str(mean(map(lambda x: x.get_error(), population))))
        # print map(lambda x: x.error, population),

        if elitism:
            children = population[:elitism]

        while len(children) < population_size:
            operator = select_genetic_operator()
            # print operator
            parent1 = selection(population)
            if operator == 'crossover':
                parent2 = selection(population)
                child1, child2 = crossover(parent1, parent2)
                children.append(child1)
                children.append(child2)
            elif operator == 'mutation':
                child1 = mutation(parent1)
                children.append(child1)
            elif operator == 'reproduction':
                child1 = reproduction(parent1)
                children.append(child1)

        evaluate_population(children, data)
        population = sorted(children, key=lambda x: x.error)[:population_size]

        s_best = population[0]

        current_generation += 1

    print('Generation: ' + str(current_generation) + ' Best:' +
          str(s_best.get_error()) + ' Mean:' +
          str(mean(map(lambda x: x.get_error(), population))))

    return s_best


def loadtxt(file, delimiter=','):
    with open(file, 'r') as f:
        return [map(float, line[:-1].split(delimiter)) for line in f]


if __name__ == '__main__':
    seed = None

    train_data = loadtxt('./datasets/keijzer-7-train.csv', delimiter=',')

    random.seed(seed)

    population_size = 10
    max_depth = 4
    generations = 50
    tournament_size = 7
    functions = [operator.add, operator.sub, operator.mul, div, math.sin,
                 math.cos]
    terminals = ['R'] + ['X' + str(i) for i in range(len(train_data[0]) - 1)]
    p_crossover = 0.9
    p_mutation = 0.05
    p_reproduction = 0.05
    elitism = 5

    node = Individual(gen_rnd_expr(functions, terminals, max_depth, True))
    node.print_tree()

    print
    new_node = mutation(node, terminals, functions)
    new_node.print_tree()
