import math
import numpy as np
from operator import truediv as div

def euc_dist_2d(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2.0 + (y1 - y2) ** 2.0)


def euc_dist(p1, p2):
    a1 = np.array(p1)
    a2 = np.array(p2)
    return np.linalg.norm(a1 - a2)


class AntColony(object):
    def __init__(self, num_ants, iterations, pher, a, b, decay):
        self.num_ants = num_ants
        self.iterations = iterations
        self.initial_pheromone = pher
        self.pher_coef = a
        self.heur_coef = b
        self.decay_factor = decay

    def set_data(self, num_points, p_median, points):
        self.num_points = num_points
        self.num_medians = p_median
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

    def __build_pheromone_matrix(self, size, initial_pheromone):
        matrix = np.full((size, ) * 2, initial_pheromone)

        return matrix

    def median_fn(self, initial_node, node):
        point = self.points[node]
        return point.get_capacity() / point.get_demand()

    def non_median_fn(self, initial_node, node):
        return

    def transition(self, initial_node, pheromone, heur_fn, all_nodes,
                   not_available=[], not_available_size=0):

        nodes = np.setdiff1d(all_nodes, not_available[:not_available_size])

        probs = np.zeros_like(nodes, dtype=float)

        for i, node in enumerate(nodes):
            pher_prob = ((pheromone[node])**self.pher_coef)
            heur_prob = (heur_fn(initial_node, node))**self.heur_coef
            probs[i] = pher_prob * heur_prob

        probs_sum = np.sum(probs)

        if probs_sum == 0:
            probs = None
        else:
            vfunc = np.vectorize(div)
            probs = vfunc(probs, probs_sum)

        return np.random.choice(nodes, p=probs)

    def __build_initial_solution(self, pheromone):
        # Add median
        init_pos = 1

        nodes = np.arange(self.num_points)
        medians = np.empty(self.num_medians, dtype=int)

        ants = np.empty(self.num_ants, dtype=int)

        solution = np.empty(self.num_medians, dtype=object)

        for i in range(len(medians)):
            next_node = self.transition(init_pos, pheromone[init_pos],
                                        self.median_fn, nodes, medians, i)
            medians[i] = next_node
            ants[i] = next_node
            # solution.add

        for i in range(self.num_medians, self.num_ants):
            next_node = self.transition(init_pos, pheromone[init_pos],
                                        self.median_fn, medians)
            ants[i] = next_node

        print(medians)

        print(ants)

        nodes = np.setdiff1d(nodes, medians)
        # next_node = transition_non_median(initial_position)
        # Add non-median

    def run(self):
        np.random.seed(1)
        self.distance_matrix = self.__build_distance_matrix(self.points)
        pher_matrix = self.__build_pheromone_matrix(self.num_points,
                                                    self.pher_coef)

        # Inicializa tij (igualmente para cada aresta)
        # Distribui cada uma das k formigas em um no selecionado aleatoriamente
        self.__build_initial_solution(pher_matrix)

        for i in range(self.iterations):
            for j in range(self.num_ants):
                # Constroi uma solucao aplicando uma regra de transicao
                # probabilistica (e-1) vezes // e e o numero de arestas do
                # grafo

                # Avalia o custo de cada solucao construida
                # solution.eval()

                # update best solution
                1

            self.update_pheromone()
