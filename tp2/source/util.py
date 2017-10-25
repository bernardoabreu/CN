from point import Point
import numpy as np


def read_input(filename):

    with open(filename, 'r') as f:
        num_points, p_median = map(int, f.readline().split())

        points = np.array([Point(*(line.split())) for line in f])

        return num_points, p_median, points
