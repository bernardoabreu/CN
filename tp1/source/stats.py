

class Stats(object):
    def __init__(self):
        self.__mean = float('inf')
        self.used = set()

        self.clear_data()
        self.reset()

    def record_data(self):
        self.mean_list.append(self.__mean)
        self.median_list.append(self.__median)
        self.cross_worse_list.append(self.__cross_worse)
        self.cross_equal_list.append(self.__cross_equal)
        self.cross_better_list.append(self.__cross_better)
        self.cross_size_list.append(self.__cross_size)
        self.best_list.append(self.__best)
        self.worst_list.append(self.__worst)
        self.repeated_list.append(self.__repeated)

    def clear_data(self):
        self.mean_list = []
        self.median_list = []
        self.cross_worse_list = []
        self.cross_equal_list = []
        self.cross_better_list = []
        self.cross_size_list = []
        self.best_list = []
        self.worst_list = []
        self.repeated_list = []

    def reset(self):
        self.__median = 0
        self.__sum = 0
        self.__size = 0
        self.__cross_worse = 0
        self.__cross_equal = 0
        self.__cross_better = 0
        self.__cross_size = 0
        self.__best = float('inf')
        self.__worst = 0.0
        self.__repeated = 0
        self.used.clear()

    def mean(self, x=None):
        if x is None:
            self.__mean = self.__sum / self.__size
        else:
            size = 0
            self.__mean = 0
            for n in x:
                self.__mean += n
                size += 1

            self.__mean /= size

        return self.__mean

    def add_median(self, child):
        self.__median = child.get_error()

    def add_crossover_child(self, child):
        fitness = child.get_error()
        self.__cross_size += 1
        if fitness > self.__mean:
            self.__cross_worse += 1
        elif fitness < self.__mean:
            self.__cross_better += 1
        else:
            self.__cross_equal += 1

    def add_child(self, child, crossover=False):
        fitness = child.get_error()

        self.__sum += fitness
        self.__size += 1

        if fitness < self.__best:
            self.__best = fitness
        elif fitness > self.__worst:
            self.__worst = fitness

        if crossover:
            self.add_crossover_child(child)

        individual = str(child)

        if individual in self.used:
            self.__repeated += 1
        else:
            self.used.add(individual)

    def print_stats(self):
        self.mean()
        print('Best fitness: ' + str(self.__best))
        print('Mean fitness: ' + str(self.__mean))
        print('Median fitness: ' + str(self.__median))
        print('Worst fitness: ' + str(self.__worst))
        print('Repeated individuals in population: ' + str(self.__repeated))
        print('Crossover children better than parent\'s mean: ' +
              str(self.__cross_better))
        print('Crossover children worse than parent\'s mean: ' +
              str(self.__cross_worse))
        print('Total of crossover children: ' +
              str(self.__cross_size))

    def dump_to_file(self, out_file):
        print out_file
        with open(out_file + '__mean.csv', 'a') as f:
            f.write(','.join(map(str, self.mean_list)) + '\n')
        with open(out_file + '__median.csv', 'a') as f:
            f.write(','.join(map(str, self.median_list)) + '\n')
        with open(out_file + '__best.csv', 'a') as f:
            f.write(','.join(map(str, self.best_list)) + '\n')
        with open(out_file + '__worst.csv', 'a') as f:
            f.write(','.join(map(str, self.worst_list)) + '\n')
        with open(out_file + '__cross_worse.csv', 'a') as f:
            f.write(','.join(map(str, self.cross_worse_list)) + '\n')
        with open(out_file + '__cross_better.csv', 'a') as f:
            f.write(','.join(map(str, self.cross_better_list)) + '\n')
        with open(out_file + '__cross_size.csv', 'a') as f:
            f.write(','.join(map(str, self.cross_size_list)) + '\n')
        with open(out_file + '__repeated.csv', 'a') as f:
            f.write(','.join(map(str, self.repeated_list)) + '\n')
            # f.write('Generation,Mean,Best Fitness,Worst Fitness,' +
            #         'Crossover children worse than parent,' +
            #         'Crossover children better than parent,' +
            #         'Repeated elements\n')
            # for i, line in enumerate(zip(self.mean_list, self.best_list,
            #                          self.worst_list, self.cross_worse_list,
            #                          self.cross_better_list,
            #                          self.repeated_list)):
            #     print line
            #     f.write(str(i) + ',' + ','.join(map(str, line)) + '\n')
