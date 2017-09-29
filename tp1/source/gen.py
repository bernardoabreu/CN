#!/usr/bin/env  python


from sys import argv


d = {
    'Best fitness': [],
    'Mean fitness': [],
    'Median fitness': [],
    'Worst fitness': [],
    'Repeated individuals in population': [],
    'Crossover children better than parent\'s mean': [],
    'Crossover children worse than parent\'s mean': [],
    'Total of crossover children': [],
    'Error': []
}

name = {
    'Best fitness': 'best',
    'Mean fitness': 'mean',
    'Median fitness': 'median',
    'Worst fitness': 'worst',
    'Repeated individuals in population': 'repeated',
    'Crossover children better than parent\'s mean': 'cross_better',
    'Crossover children worse than parent\'s mean': 'cross_worse',
    'Total of crossover children': 'cross_size',
    'Error': 'test_best',
}


filename = argv[1]
dataset = argv[2]

with open(filename, 'r') as f:
    lines = f.read().splitlines()
    for line in lines:
        cur = line.split(':')

        if len(cur) == 2:
            if cur[0] in d:
                d[cur[0]].append(cur[1].strip())

# print d


for k, v in d.iteritems():
    with open(dataset + '__' + name[k], 'a') as f:
        f.write(','.join(v) + '\n')
