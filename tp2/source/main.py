#!/usr/bin/env python3

import numpy as np
from aco import AntColony
import argparse


def read_input(filename):
    with open(filename, 'r') as f:
        num_points, p_median = map(int, f.readline().split())
    points = np.loadtxt(filename, skiprows=1)
    return num_points, p_median, points


def main(args):
    filename = args.file
    num_ants = args.ants
    iterations = args.iterations
    pher = 0.5
    a = args.a
    b = args.b
    decay = args.decay
    seed = args.seed
    stats = args.stats

    num_points, p_median, points = read_input(filename)

    aco = AntColony(num_ants, iterations, pher, a, b, decay, seed=seed,
                    stat_file=stats)
    aco.set_data(num_points, p_median, points)

    solution = aco.run()

    print('Best distance: ' + str(solution))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True,
                        help='Input file.')
    parser.add_argument('--ants', type=int, default=10,
                        help='Number of ants.')
    parser.add_argument('--iterations', type=int, default=100,
                        help='Number of iterations.')
    parser.add_argument('-a', type=int, default=3,
                        help='Alpha. Influence of the pheromone.')
    parser.add_argument('-b', type=int, default=1,
                        help='Beta. Influence of the heuristic function.')
    parser.add_argument('--decay', type=float, default=0.1,
                        help='Seed for random number generator')
    parser.add_argument('--seed', type=int, default=None,
                        help='Seed for random number generator')
    parser.add_argument('--stats', default='',
                        help='File to save statistics.')

    args = parser.parse_args()
    # print(args)

    main(args)
