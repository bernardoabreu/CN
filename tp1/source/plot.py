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


def line_mean_plot(a, y_label, save=''):
    means = []
    for column in a.T:
        means.append(np.mean(column))
    a_means = np.array(means)
    plt.plot(np.arange(len(a_means)), a_means)
    plt.xlabel('generations')
    plt.ylabel(y_label)
    plt.title(y_label + ' x ' + 'generations')
    plt.grid(True)

    figure = plt.gcf()
    figure.set_size_inches(19, 12)
    if save:
        # when saving, specify the DPI
        print 'saving to ' + save
        plt.savefig(save + '_line.png', dpi=300)
    # plt.show()


def line_plot(a, y_label, save=''):
    plt.plot(np.arange(len(a)), a)
    plt.xlabel('generations')
    plt.ylabel(y_label)
    plt.title(y_label + ' x ' + 'generations')
    plt.grid(True)

    figure = plt.gcf()
    figure.set_size_inches(19, 12)
    if save:
        # when saving, specify the DPI
        print 'saving to ' + save
        plt.savefig(save + '_line.png', dpi=300)
    plt.show()


def boxplot(a, y_label, save=''):
    df = DataFrame(a)
    plt.figure()
    df.boxplot()
    plt.xlabel('generations')
    plt.ylabel(y_label)
    plt.title(y_label + ' x ' + 'generations')
    plt.grid(True)
    figure = plt.gcf()
    figure.set_size_inches(19, 12)
    if save:
        print 'saving to ' + save
        plt.savefig(save + '_boxplot.png', dpi=300)
    # plt.show()


if __name__ == '__main__':
    print 'running'
    in_file = argv[1]

    label = in_file.split('.')[0].split('__')[-1]
    a = loadtxt(in_file)

    outputfolder = argv[2] + '/' + label if len(argv) > 2 else ''

    # boxplot(a, label, outputfolder)
    # line_mean_plot(a, label, outputfolder)
    line_plot(a, label)
