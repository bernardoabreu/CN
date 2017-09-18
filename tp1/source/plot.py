import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

def loadtxt(file, delimiter=','):
    with open(file, 'r') as f:
        return [list(map(float, line[:-1].split(delimiter))) for line in f]


def read_csv(outfile):
    # a = np.genfromtxt(outfile, delimiter=',', names=True,)
    #                   converters={'inf': float('inf')})
    # print a
    # print a.dtype.names
    means = loadtxt(outfile)

    a = np.array(means)
    print a

    means_of_means = []
    stds = []
    max_min = []
    for column in a.T:
        means_of_means.append(np.mean(column))
        stds.append(np.std(column))
        if np.mean(column) - np.std(column) < 0:
            print 'cu'
        # max_.append(np.max(column))
        # min_.append(np.min(column))

    a_means = np.array(means_of_means)
    a_stds = np.array(stds)
    # a_max_min = np.array(max_min)

    # construct some data like what you have:
    # x = np.random.randn(100, 8)
    # mins = x.min(0)
    # maxes = x.max(0)
    # means = x.mean(0)
    # std = x.std(0)

    print stds
    print max_min

    # df = DataFrame(means)
    # plt.figure()
    # df.boxplot()

    # create stacked errorbars:
    # plt.errorbar(np.arange(8), means, [means - mins, maxes - means],
    #              fmt='.k', ecolor='gray', lw=1)
    # plt.errorbar(np.arange(8), means, std, fmt='ok', lw=5)
    # plt.xlim(-1, 8)
    # plt
    # plt.errorbar(np.arange(len(a_means)), a_means, a_max_min,
    #              fmt='.k', ecolor='gray', lw=1)
    plt.errorbar(np.arange(len(a_means)), a_means, a_stds, fmt='ok', lw=5)
    # plt.xlim(-1, 8)

    # n = np.loadtxt(outfile, delimiter=',', skiprows=1)
    # print n.dtype
    # print n[:,0]
    # print n[:,3]
    # plt.plot(np.arange(len(a_means)), a_means)
    # plt.xlabel('Generations')
    # plt.ylabel('Means')
    # # plt.title(names[3] + ' x ' + names[0])
    # plt.grid(True)
    # plt.savefig("test.png")
    plt.show()


from sys import argv


read_csv(argv[1])
