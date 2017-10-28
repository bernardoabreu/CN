import numpy as np


def euc_dist(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


class AntColony(object):
    def __init__(self, num_ants, iterations, pher, a, b, decay, seed=None):
        self.num_ants = num_ants
        self.iterations = iterations
        self.initial_pheromone = pher
        self.pher_coef = a
        self.heur_coef = b
        self.decay_factor = decay

        self.pher_max = 0.999
        self.pher_min = 0.001

        np.random.seed(seed)

    def set_data(self, num_points, p_median, points):
        self.num_points = num_points
        self.num_medians = p_median
        self.num_clients = num_points - p_median
        self.points = points

    def __build_pheromone_vector(self):
        self.pheromone = np.full(self.num_points, self.initial_pheromone,
                                 dtype=float)

    def __build_distance_matrix(self, points):
        num_points = points.shape[0]
        matrix = np.zeros((num_points,) * 2)

        for i in range(num_points):
            for j in range(i + 1, num_points):
                dist = euc_dist(points[i].get_coord(), points[j].get_coord())
                matrix[i][j] = dist
                matrix[j][i] = dist

        return matrix

    def __gap(self, clients, medians):

        x = np.zeros((self.num_points,) * 2, dtype=int)

        capacities = np.array([self.points[m].get_capacity() for m in medians])

        indices = np.argsort(np.amin(self.distances[np.ix_(clients, medians)],
                                     axis=1))
        ordered_clients = clients[indices]

        for i in range(self.num_clients):
            cur_client = ordered_clients[i]

            indices = np.argsort(self.distances[cur_client][medians])
            ordered_medians = medians[indices]
            ordered_capacities = capacities[indices]

            for j in range(self.num_medians):
                cur_median = ordered_medians[j]
                demand = self.points[cur_client].get_demand()

                if (ordered_capacities[j] - demand) >= 0:
                    ordered_capacities[j] -= demand
                    x[cur_client][cur_median] = 1
                    break

        return x

    def __alocate(self, cur_node, ordered_nodes):
        all_nodes = 0
        sum_distance = 0.0

        for dist in self.distances[cur_node][ordered_nodes]:
            if sum_distance + dist > self.points[cur_node].get_capacity():
                break
            sum_distance += dist
            all_nodes += 1

        return all_nodes, sum_distance

    def __density(self):
        nodes = np.arange(1, self.num_points)
        density = np.empty(self.num_points)

        nodes_size = self.num_points - 1

        for i in range(nodes_size):
            ordered_nodes = nodes[np.argsort(self.distances[i][nodes])]
            all_nodes, sum_distance = self.__alocate(i, ordered_nodes)
            density[i] = all_nodes / sum_distance

            nodes[i] = i

        ordered_nodes = nodes[np.argsort(self.distances[nodes_size][nodes])]
        all_nodes, sum_distance = self.__alocate(nodes_size, ordered_nodes)
        density[nodes_size] = all_nodes / sum_distance

        return density

    def transition(self, all_nodes, not_available=[]):
        # print('not_available:', not_available)
        nodes = np.setdiff1d(all_nodes, not_available)

        probs = (self.pheromone[nodes] ** self.pher_coef) * \
            (self.heur_values[nodes] ** self.heur_coef)

        probs_sum = np.sum(probs)

        probs = probs / probs_sum if probs_sum else None

        return np.random.choice(nodes, p=probs)

    def build_solution(self):

        nodes = np.arange(self.num_points)
        medians = np.empty(self.num_medians, dtype=int)

        for i in range(self.num_medians):
            next_node = self.transition(nodes, medians[:i])
            medians[i] = next_node

        clients = np.setdiff1d(nodes, medians)

        assign_matrix = self.__gap(clients, medians)

        return assign_matrix

    def eval(self, assign_matrix):
        distance = np.sum(assign_matrix * self.distances)
        medians = np.nonzero(np.sum(assign_matrix, axis=0))[0]
        return distance, medians

    def __converged_pheromone(self):
        converged_value = self.num_medians * self.pher_max + \
            self.num_clients * self.pher_min

        if round(np.sum(self.pheromone), 2) == round(converged_value, 2):
            self.pheromone.fill(self.initial_pheromone)

    def update_pheromone(self, local_best, local_worst, global_best):
        update_points = np.union1d(local_best[1], global_best[1])

        local_sub = local_worst - local_best[0]
        if local_sub == 0.0:
            local_sub = 0.001

        update_delta = 1.0 - ((local_best[0] - global_best[0]) / local_sub)

        update_decay = (1.0 - self.decay_factor)
        update_value = self.decay_factor * update_delta

        self.pheromone *= update_decay
        self.pheromone[update_points] += update_value

        np.clip(self.pheromone, self.pher_min, self.pher_max,
                out=self.pheromone)

        self.__converged_pheromone()

    def __local_edges(self, sol_dist, sol_medians):
        best_index = np.argmin(sol_dist)

        local_best = (sol_dist[best_index], sol_medians[best_index])
        local_worst = np.amax(sol_dist)

        return local_best, local_worst

    def run(self):
        self.distances = self.__build_distance_matrix(self.points)
        self.heur_values = self.__density()

        self.__build_pheromone_vector()

        global_best = self.eval(self.build_solution())
        sol_dist = np.empty(self.num_ants)
        sol_medians = np.empty(self.num_ants, dtype=object)

        for i in range(self.iterations):
            for j in range(self.num_ants):
                solution_matrix = self.build_solution()
                sol_dist[j], sol_medians[j] = self.eval(solution_matrix)

            local_best, local_worst = self.__local_edges(sol_dist, sol_medians)
            self.update_pheromone(local_best, local_worst, global_best)

            print('Iteration ' + str(i + 1) + ':')
            print('Global Best: ' + str(global_best[0]))
            print('Local Best: ' + str(local_best[0]))
            print('Local worst: ' + str(local_worst))
            print()

            if local_best[0] < global_best[0]:
                global_best = local_best

        return global_best[0]
