import math
import numpy as np
from cluster import Cluster
from operator import truediv as div


def euc_dist_2d(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2.0 + (y1 - y2) ** 2.0)


def euc_dist(p1, p2):
    a1 = np.array(p1)
    a2 = np.array(p2)
    return np.linalg.norm(a1 - a2)


class AntColony(object):
    def __init__(self, num_ants, iterations, pher, a, b, decay, seed=None):
        self.num_ants = num_ants
        self.iterations = iterations
        self.initial_pheromone = pher
        self.pher_coef = a
        self.heur_coef = b
        self.decay_factor = decay
        np.random.seed(seed)

        self.__v_div_func = np.vectorize(div)
        self.__v_transit_func = np.vectorize(self.__transtion_prob)

    def __build_pheromone_vector(self):
        self.pheromone = np.full(self.num_points, self.pher_coef)

    def set_data(self, num_points, p_median, points):
        self.num_points = num_points
        self.num_medians = p_median
        self.num_clients = num_points - p_median
        self.points = points

    def update_pheromone(self):
        return

    def __build_distance_matrix(self, points):
        num_points = points.shape[0]
        matrix = np.zeros((num_points,) * 2)
        print(matrix)

        for i in range(num_points):
            for j in range(i + 1, num_points):
                dist = euc_dist(points[i].get_coord(), points[j].get_coord())
                matrix[i][j] = dist
                matrix[j][i] = dist

        return matrix

    def heur_fn(self):
        return

    def __transtion_prob(self, node):
        return (self.pheromone[node] ** self.pher_coef) * \
            1.0  # (self.heur_fn(initial_node, node) ** self.heur_coef)

    def transition(self, all_nodes, not_available=[]):
        # print('not_available:', not_available)
        nodes = np.setdiff1d(all_nodes, not_available)

        probs = self.__v_transit_func(nodes)
        # print('probs:', probs)

        probs_sum = np.sum(probs)
        # print('probs_sum:', probs_sum)

        probs = self.__v_div_func(probs, probs_sum) if probs_sum else None

        # print('probs:', probs)
        return np.random.choice(nodes, p=probs)

    def __gap(self, clients, medians):
        ordered_clients = sort_clients(clients)

        for i in range(self.num_clients):
            ordered_medians = sort_medians(medians, ordered_clients[i])

            for j in range(self.num_medians):
                if (ordered_medians[j].get_capacity() -
                    ordered_clients.get_demand()):
                    x[ordered_clients[i]][ordered_medians[j]] = 1
        return

    def __build_solution(self):

        nodes = np.arange(self.num_points)
        medians = np.empty(self.num_medians, dtype=int)

        for i in range(self.num_medians):
            next_node = self.transition(nodes, medians[:i])
            medians[i] = next_node

        print('medians:', medians)

        clients = np.setdiff1d(nodes, medians)
        print(clients)

        # print('ants:', ants)

    def run(self):
        self.distances = self.__build_distance_matrix(self.points)

        # Inicializa tij (igualmente para cada aresta)
        self.__build_pheromone_vector()

        # Distribui cada uma das k formigas em um no selecionado aleatoriamente
        self.__build_solution()

        # for i in range(self.iterations):
        #     for j in range(self.num_ants):
        #         self.__build_solution()

        #     self.update_pheromone()
