import math
from point import Point
import numpy as np


def read_input(filename):

    with open(filename, 'r') as f:
        num_points, p_median = map(int, f.readline().split())

        points = np.array([Point(*(line.split())) for line in f])

        return num_points, p_median, points


def euc_dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2.0 + (y1 - y2) ** 2.0)


def build_distance_matrix(points):
    num_points = points.shape[0]
    matrix = np.zeros([num_points, num_points])

    for i in range(num_points):
        for j in range(i + 1, num_points):
            matrix[i][j] = euc_dist(points[i].get_x(), points[i].get_y(),
                                    points[j].get_x(), points[j].get_y())
            matrix[j][i] = matrix[i][j]

    return matrix
