#!/usr/bin/env  python

import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd
from pandas import DataFrame
from sys import argv


def loadtxt(file, delimiter=','):
    with open(file, 'r') as f:
        return np.array([list(map(float, line[:-1].split(delimiter)))
                        for line in f])


def lineplot(a, y_label):
    means = []
    for column in a.T:
        means.append(np.mean(column))
    a_means = np.array(means)
    plt.plot(np.arange(len(a_means)), a_means)
    plt.xlabel('generations')
    plt.ylabel(y_label)
    plt.title(y_label + ' x ' + 'generations')
    plt.grid(True)
    plt.show()


def boxplot(a, y_label):
    df = DataFrame(a)
    plt.figure()
    df.boxplot()
    plt.xlabel('generations')
    plt.ylabel(y_label)
    plt.title(y_label + ' x ' + 'generations')
    plt.grid(True)
    # plt.savefig("test.png")
    plt.show()


if __name__ == '__main__':

    in_file = argv[1]
    label = argv[2]

    a = loadtxt(in_file)

    boxplot(a, label)
    boxplot(a, label)
