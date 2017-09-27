#!/usr/bin/env python

import random
import copy
from individual import Individual

from functions import UNARY

from node import FunctionNode
from node import TerminalNode
from stats import Stats


class GeneticProgramming(object):
    """[summary]

    [description]
    """
    def __init__(self, max_depth, functions, terms, p_crossover, p_mutation):
        self.max_depth = max_depth
        self.functions = functions
        self.terminals = terms
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation

        self.initialize_population = self.__ramped_half_and_half
        self.selection = self.__tournament_selection

        self.__full = True
        self.tournament_size = 3

        self.stats = Stats()

    def set_random_seed(self, seed):
        random.seed(seed)

    def set_tournament_size(self, tournament_size):
        self.tournament_size = tournament_size

    def set_probabilities(self, p_crossover, p_mutation):
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation

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
        """[summary]

        [description]

        Arguments:
            population_size {[type]} -- [description]
            max_depth {[type]} -- [description]
            funcs {[type]} -- [description]
            terms {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        pop = []
        group = (population_size / (max_depth - 1))
        full = True

        for i in range(2, max_depth + 1):
            for j in range(int(group)):
                pop.append(Individual(self.__gen_rnd_expr(funcs,
                                                          terms, i, full)))
                full = not full

        for i in range(population_size % (max_depth - 1)):
            pop.append(Individual(self.__gen_rnd_expr(funcs, terms, max_depth,
                                  full)))

        return pop

    def __simple_initialization(self, pop_size, max_depth, funcs, terms):
        return [Individual(self.__gen_rnd_expr(funcs, terms, max_depth,
                self.__full)) for i in range(pop_size)]

    def set_selection(self, selection_type):
        if selection_type == 'tournament':
            self.selection = self.__tournament_selection

    def __get_best_solution(self, population):
        return min(population, key=(lambda individual: individual.get_error()))

    def __tournament_selection(self, population):
        sample = random.sample(population, self.tournament_size)
        return self.__get_best_solution(sample)

    def __gen_rnd_function(self, func, func_set, term_set, max_depth):
        child_left = self.__gen_rnd_expr(func_set, term_set, max_depth - 1)
        child_right = None if func in UNARY else \
            self.__gen_rnd_expr(func_set, term_set, max_depth - 1)

        return FunctionNode(func, child_left, child_right)

    def __gen_rnd_expr(self, func_set, term_set, max_depth, full=False):
        node = None
        length = len(term_set) + len(func_set)
        rand = random.randrange(length)

        if max_depth == 0 or ((not full) and rand < len(term_set)):
            term = random.choice(term_set)

            if term == 'R':
                term = random.randint(-5, 5)

            node = TerminalNode(term)
        else:
            func = random.choice(func_set)

            node = self.__gen_rnd_function(func, func_set, term_set, max_depth)

        return node

    def __select_genetic_operator(self):
        p = random.random()

        if p > (self.p_crossover + self.p_mutation):
            return 'reproduction'
        else:
            return 'mutation' if p > self.p_crossover else 'crossover'

    def evaluate_population(self, population, data):
        for individual in population:
            individual.eval(data, self.max_depth)

    def crossover(self, parent1, parent2):
        """[summary]

        [description]

        Arguments:
            parent1 {[type]} -- [description]
            parent2 {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
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
        """[summary]

        [description]

        Arguments:
            parent {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        mutant = copy.deepcopy(parent)
        mutant_list = mutant.get_list()

        element = random.choice(mutant_list)
        content = element.get_content()
        element_right = element.get_right_child()

        is_function = isinstance(element, FunctionNode)
        terminals = [i for i in self.terminals if i != content]
        functions = [i for i in self.functions if i != content]

        length = len(terminals) + len(functions)
        rand = random.randrange(length)

        if rand < len(terminals):
            term = terminals[rand]

            if term == 'R':
                term = random.choice(
                    [n for n in range(-5, 6) if n != content])

            # print('term', term)
            if is_function:
                # print 'Replace function with terminal'
                node = TerminalNode(term)
                mutant.replace_node(element, node)
            else:
                # print 'Replace terminal'
                element.set_content(term)
        else:
            func = functions[rand - len(terminals)]
            # print 'func', func

            depth = 1

            if is_function:
                # print 'Replace terminal'
                if func in UNARY:
                    if element_right is not None:
                        element.set_right_child(None)
                elif element_right is None:
                    element.set_right_child(self.__gen_rnd_function(func,
                                            self.functions, self.terminals,
                                            depth))
                element.set_content(func)
            else:
                # print 'Replace terminal with function'
                node = self.__gen_rnd_function(func, self.functions,
                                               self.terminals, depth)
                mutant.replace_node(element, node)

        return mutant

    def reproduction(self, parent):
        return copy.deepcopy(parent)

    def save_stats(self, out_file):
        self.stats.dump_to_file(out_file)

    def run(self, data, pop_size, generations, elitism=0):

        population = self.initialize_population(pop_size, self.max_depth,
                                                self.functions, self.terminals)
        print('Population size: ' + str(len(population)) + '\n')
        self.evaluate_population(population, data)
        population.sort(key=lambda x: x.get_error())
        # s_best = self.get_best_solution(population)
        s_best = population[0]

        print('Initial population:')
        for p in population:
            print(p)
            self.stats.add_child(p)

        print('\n')

        current_generation = 0

        while current_generation < generations and s_best.get_error() > 0.0:
            print('Generation ' + str(current_generation) + ':')
            self.stats.mean()
            self.stats.print_stats()
            print('\n')
            self.stats.record_data()
            self.stats.reset()

            children = []

            if elitism:
                children = population[:elitism]

            while len(children) < pop_size:
                operator = self.__select_genetic_operator()
                # print operator
                parent1 = self.selection(population)
                if operator == 'crossover':
                    parent2 = self.selection(population)
                    child1, child2 = self.crossover(parent1, parent2)
                    child1.eval(data, self.max_depth)
                    child2.eval(data, self.max_depth)
                    self.stats.add_child(child1, crossover=True)
                    self.stats.add_child(child2, crossover=True)
                    children.append(child1)
                    children.append(child2)
                elif operator == 'mutation':
                    child1 = self.mutation(parent1)
                    child1.eval(data, self.max_depth)
                    self.stats.add_child(child1)
                    children.append(child1)
                elif operator == 'reproduction':
                    child1 = self.reproduction(parent1)
                    self.stats.add_child(child1)
                    children.append(child1)

            # self.evaluate_population(children, data)

            population = sorted(children, key=lambda x: x.get_error())[:pop_size]

            self.stats.add_median(population[len(population)//2])
            s_best = population[0]

            current_generation += 1

        print('Generation ' + str(current_generation) + ':')
        self.stats.mean()
        self.stats.print_stats()
        self.stats.record_data()

        return s_best
