import numpy as np
from sys import maxsize as MAXSIZE


class Stats(object):
    """ Stores and calculates statistics. """
    def __init__(self, max_global=MAXSIZE):
        self.max_global = max_global
        self.reset()

    def record_data(self):
        if self.__local_best < self.__global_best:
            self.__global_best = self.__local_best
            self.global_medians = self.__local_medians

        self.best_list.append(self.__local_best)
        self.worst_list.append(self.__local_worst)
        self.mean_list.append(self.__mean)
        self.median_list.append(self.__median)
        self.global_best_list.append(self.__global_best)
        self.repeated_list.append(self.__repeated)
        self.local_medians_list.append(self.__local_medians)

    def clear_data(self):
        self.mean_list = []
        self.median_list = []
        self.best_list = []
        self.worst_list = []
        self.global_best_list = []
        self.repeated_list = []
        self.local_medians_list = []

    def reset(self):
        self.__mean = 0.0
        self.__median = 0.0
        self.__global_best = self.max_global
        self.__local_best = 0.0
        self.__local_worst = 0.0
        self.__repeated = 0
        self.__local_medians = None
        self.global_medians = np.array([], dtype=int)
        self.clear_data()

    def add_solution(self, solution, medians):
        best_index = np.argmin(solution)

        self.__local_best = solution[best_index]
        self.__local_medians = medians[best_index]
        self.__local_worst = np.amax(solution)
        self.__mean = np.mean(solution)
        self.__median = np.median(solution)
        self.__repeated = len(solution) - len(np.unique(solution))

    def print_stats(self):
        print('Global Best: ' + str(self.__global_best))
        print('Local Best: ' + str(self.__local_best))
        print('Local worst: ' + str(self.__local_worst))
        print('Mean: ' + str(self.__mean))
        print('Median: ' + str(self.__median))
        print('Repeated: ' + str(self.__repeated))
        print()

    def dump_to_file(self, out_file):
        with open(out_file + '__mean.csv', 'a') as f:
            f.write(','.join(map(str, self.mean_list)) + '\n')
        with open(out_file + '__median.csv', 'a') as f:
            f.write(','.join(map(str, self.median_list)) + '\n')
        with open(out_file + '__best.csv', 'a') as f:
            f.write(','.join(map(str, self.best_list)) + '\n')
        with open(out_file + '__worst.csv', 'a') as f:
            f.write(','.join(map(str, self.worst_list)) + '\n')
        with open(out_file + '__global_best.csv', 'a') as f:
            f.write(','.join(map(str, self.global_best_list)) + '\n')
        with open(out_file + '__repeated.csv', 'a') as f:
            f.write(','.join(map(str, self.repeated_list)) + '\n')

    def get_local_best(self):
        return (self.__local_best, self.__local_medians)

    def get_local_worst(self):
        return self.__local_worst

    def get_global_best(self):
        return (self.__global_best, self.global_medians)
