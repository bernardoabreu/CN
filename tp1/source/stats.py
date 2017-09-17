
class Stats(object):
    def __init__(self):
        self.__mean = float('inf')
        self.used = set()
        self.reset()

    def reset(self):
        self.__sum = 0
        self.__size = 0
        self.__cross_worse = 0
        self.__cross_equal = 0
        self.__cross_better = 0
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

    def add_crossover_child(self, child):
        fitness = child.get_error()
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
        print('Worst fitness: ' + str(self.__worst))
        print('Repeated individuals in population: ' + str(self.__repeated))
        print('Crossover children better than parent\'s mean: ' +
              str(self.__cross_better))
        print('Crossover children worse than parent\'s mean: ' +
              str(self.__cross_worse))
