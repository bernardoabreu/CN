#!/usr/bin/env python3

from point import Point
import numpy as np
from aco import AntColony
import sys


def read_input(filename):

    with open(filename, 'r') as f:
        num_points, p_median = map(int, f.readline().split())

        points = np.array([Point(*(line.split())) for line in f])

        return num_points, p_median, points


if __name__ == '__main__':
    filename = sys.argv[1]
    num_points, p_median, points = read_input(filename)

    num_ants = 90
    iterations = 10
    pher = 0.1
    a = 0.1
    b = 0.1
    decay = 0.1

    aco = AntColony(num_ants, iterations, pher, a, b, decay, seed=1)
    aco.set_data(num_points, p_median, points)

    aco.run()
    # print(aco.distance_matrix)
