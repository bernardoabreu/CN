#!/usr/bin/env  python

from functions import *
from genetic_programming import GeneticProgramming
import argparse


def loadtxt(file, delimiter=','):
    with open(file, 'r') as f:
        return [list(map(float, line[:-1].split(delimiter))) for line in f]


def main(args):
    seed = args.seed
    train_file = args.train
    test_file = args.test
    population_size = args.pop_size
    generations = args.gen
    tournament_size = args.tournament
    elitism = args.elitism
    p_crossover = args.crossover
    p_mutation = args.mutation

    max_depth = 7

    train_data = loadtxt(train_file, delimiter=',')

    funcs = [add, sub, mul, div, log, math.sin, math.cos, sqrt, power]
    terms = ['R'] + ['X' + str(i) for i in range(len(train_data[0]) - 1)]

    gp = GeneticProgramming(max_depth, funcs, terms, p_crossover, p_mutation)
    gp.set_random_seed(seed)
    gp.set_tournament_size(tournament_size)

    best = gp.run(train_data, population_size, generations, elitism)

    if args.stats:
        gp.save_stats(args.stats)

    print('\nTrain data: ' + train_file)
    print('Best error: ' + str(best.get_error()))
    print('Individual:\n' + str(best))

    test_data = loadtxt(test_file, delimiter=',')

    best.eval(test_data)
    print('\nTest data: ' + test_file)
    print('Error: ' + str(best.get_error()))

    if args.test_out:
        with open(args.test_out + '__test_best.csv', 'a') as f:
            f.write(str(best.get_error()) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', required=True,
                        help='File to train GP.')
    parser.add_argument('--test', required=True,
                        help='File to test GP.')
    parser.add_argument('--crossover', type=float, default=0.9,
                        help='Probability of crossover.')
    parser.add_argument('--mutation', type=float, default=0.1,
                        help='Probability of mutation.')
    parser.add_argument('--elitism', type=int, default=1,
                        help='Number of individuals to be used in elitism.\
                        If 0 there is no elitism.')
    parser.add_argument('--pop_size', type=int, default=50,
                        help='Size of the population')
    parser.add_argument('--gen', type=int, default=50,
                        help='Number of generations')
    parser.add_argument('--tournament', type=int, default=2,
                        help='Number of individuals to be used in tournament')
    parser.add_argument('--seed', type=int, default=None,
                        help='Seed for random number generator')
    parser.add_argument('--stats',
                        help='File to save statistics.')
    parser.add_argument('--test_out',
                        help='File to save the test data result.')

    args = parser.parse_args()
    print(args)

    main(args)
