#!/usr/bin/env python


import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd
from pandas import DataFrame
from sys import argv

from matplotlib.legend_handler import HandlerLine2D


params = {
    'legend.fontsize': 'x-large',
    'figure.figsize': (20, 15),
    'axes.labelsize': 'x-large',
    'axes.titlesize': 'x-large',
    'xtick.labelsize': 'x-large',
    'ytick.labelsize': 'x-large'
}
plt.rcParams.update(params)


def loadtxt(file, delimiter=','):
    with open(file, 'r') as f:
        return np.array([list(map(float, line[:-1].split(delimiter)))
                        for line in f])


def line_mean_plot(files, labels, y_label, save='', log=False):
    mm = []

    for file in files:
        # print(i)
        a = np.loadtxt(file)
        means = []
        for column in a.T:
            means.append(np.mean(column))
        mm.append(np.array(means))

    fig = plt.figure(figsize=(19, 11))
    ax = fig.add_subplot(111)
    plt.grid(True)

    title = y_label.replace('_', ' ').title()
    plt.xlabel('Iterations')
    plt.ylabel(title)
    plt.title(title + ' x Iterations')

    line1 = None
    for m, d in zip(mm, labels):
        line1, = plt.plot(m, label=str(d))
        print(str(d) + ': ' + str(np.mean(m)))

    if log:
        ax.set_yscale('log')

    if len(labels) > 0:
        plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})

    if save:
        print('saving to ' + save)
        plt.savefig(save + '_' + y_label + '_mean.png', dpi=fig.dpi)

    plt.show()


def line_plot(a, y_label, save=''):
    title = y_label.replace('_', ' ').title()
    plt.plot(np.arange(len(a)), a)
    plt.xlabel('Iterations')
    plt.ylabel(title)
    plt.title(title + ' x Iterations')
    plt.grid(True)

    if save:
        print('saving to ' + save)
        plt.savefig(save + '_line.png', dpi=300)
    plt.show()


def boxplot(a, y_label, save=''):
    fig = plt.figure(figsize=(19, 5))
    plt.locator_params(axis='x', nticks=10)
    df = DataFrame(a)
    plt.figure()
    df.boxplot().set_xticklabels(
        [str(i) if i % 5 == 0 else '' for i in range(101)])

    plt.xlabel('Iterations')
    plt.ylabel(y_label.title())
    plt.title(y_label.title() + ' x Iterations')
    plt.grid(True)

    if save:
        print('saving to ' + save)
        plt.savefig(save + '_boxplot.png', dpi=fig.dpi)


if __name__ == '__main__':
    print('running')

    # in_file = argv[1]

    # label = in_file.split('.')[0].split('__')[-1]
    # a = loadtxt(in_file)

    # outputfolder = argv[2] + '/' + label if len(argv) > 2 else ''

    # if len(argv) < 4:
    #     print("no")
    #     line_mean_plot(a, label, outputfolder)
    # else:
    #     t = argv[3]

    #     if t == 'boxplot':
    #         boxplot(a, label, outputfolder)
    #     elif t == 'mean':
    #         line_mean_plot(a, label, outputfolder)
    #     elif t == 'line':
    #         line_plot(a, label)

    y_label = argv[1]
    outfile = argv[2]

    size = (len(argv) - 3) / 2
    files = argv[3: 3 + size]
    labels = argv[3 + size:]

    line_mean_plot(files, labels, y_label, save='', log=False)
