#!/usr/bin/env  python

from functions import *
from genetic_programming import Genetic_Programming


def loadtxt(file, delimiter=','):
    with open(file, 'r') as f:
        return [map(float, line[:-1].split(delimiter)) for line in f]


def main():
    seed = None

    # train_data = loadtxt('./datasets/keijzer-10-train.csv', delimiter=',')
    train_data = loadtxt('./datasets/house-train.csv', delimiter=',')

    population_size = 100
    max_depth = 7
    generations = 50
    tournament_size = 7
    functions = [operator.add, operator.sub, operator.mul, div, log, math.sin,
                 math.cos]
    terminals = ['R'] + ['X' + str(i) for i in range(len(train_data[0]) - 1)]
    p_crossover = 0.9
    p_mutation = 0.05
    p_reproduction = 0.05
    elitism = 5

    gp = Genetic_Programming(max_depth, functions, terminals, p_crossover,
                             p_mutation, p_reproduction)
    gp.set_random_seed(seed)
    gp.set_tournament_size(tournament_size)

    best = gp.run(train_data, population_size, generations, elitism)

    print 'Best', best.get_error()
    best.print_tree()

    # test_data = loadtxt('./datasets/keijzer-10-test.csv', delimiter=',')
    test_data = loadtxt('./datasets/house-test.csv', delimiter=',')

    best.eval(test_data)
    print best.get_error()


if __name__ == '__main__':
    main()
