#!/usr/bin/env  python


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


def line_mean_plot(a, y_label, save=''):
    means = []
    for column in a.T:
        means.append(np.mean(column))
    a_means = np.array(means)
    print a_means
    plt.plot(np.arange(len(a_means) - 1), a_means[1:])
    plt.xlabel('Generations')
    plt.ylabel(y_label.title())
    plt.title(y_label.title() + ' x Generations')
    plt.grid(True)

    if save:
        print('saving to ' + save)
        plt.savefig(save + '_line_mean.png', dpi=300)
    else:
        plt.show()


def line_plot(a, y_label, save=''):
    plt.plot(np.arange(len(a)), a)
    plt.xlabel('generations')
    plt.ylabel(y_label.title())
    plt.title(y_label.title() + ' x Generations')
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

    plt.xlabel('Generations')
    plt.ylabel(y_label.title())
    plt.title(y_label.title() + ' x Generations')
    plt.grid(True)

    if save:
        print('saving to ' + save)
        plt.savefig(save + '_boxplot.png', dpi=fig.dpi)



if __name__ == '__main__':
    # print('running')
    # in_file = argv[1]

    # label = in_file.split('.')[0].split('__')[-1]
    # a = loadtxt(in_file)

    # outputfolder = argv[2] + '/' + label if len(argv) > 2 else ''
    # print len(argv)
    # if len(argv) < 4:
    #     print "no"
    #     line_mean_plot(a, label, outputfolder)
    # else:
    #     t = argv[3]

    #     if t == 'boxplot':
    #         # print 'box'
    #         boxplot(a, label, outputfolder)
    #     elif t == 'mean':
    #         line_mean_plot(a, label, outputfolder)
    #     elif t == 'line':
    #         line_plot(a, label)

    print argv
    label = argv[1]
    outfile = argv[2]

    fig = plt.figure(figsize=(19, 11))
    ax = fig.add_subplot(111)
    plt.grid(True)

    if label != 'test':
        plt.xlabel('Generations')
        plt.ylabel(label.title())
        plt.title(label.title() + ' x Generations')
        if 'cross' in label:
            mm = []

            for i in argv[3:]:
                print i
                a = loadtxt(i)
                size = loadtxt(i.replace('__cross_best', '__cross_size')
                                .replace('__cross_worse', '__cross_size'))
                c = np.divide(a, size)
                means = []
                for column in c.T:
                    means.append(np.mean(column))
                mm.append(np.array(means))

            # line1, = plt.plot(mm[0][1:], label='500')

            line1 = None
            for m, d in zip(mm, [3, 7]):
                line1, = plt.plot(m, marker='o', label=str(d))

            plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})

            # figure.set_size_inches(20, 15)
            plt.savefig(outfile + '_' + label + '_mean.png', dpi=fig.dpi)
            plt.show()
        else:
            mm = []

            for i in argv[3:]:
                print i
                a = loadtxt(i)
                means = []
                for column in a.T:
                    means.append(np.mean(column))
                mm.append(np.array(means))

            # line1, = plt.plot(mm[0][1:], label='500')

            line1 = None
            for m, d in zip(mm, ['best mut-high', 'mean mut-high', 'worst mut-high',
                'best mut-low', 'mean mut-low', 'worst mut-low']):
                line1, = plt.plot(m, marker='o', label=str(d))

            ax.set_yscale('log')

            plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})

            # figure.set_size_inches(20, 15)
            plt.savefig(outfile + '_' + label + '_mean.png', dpi=fig.dpi)
            plt.show()

    else:
        plt.xlabel('Seed')
        plt.ylabel('Best fitness')
        plt.title('Best fitness x Seed')
        mm = []
        testbest = []

        for i in argv[3:]:
            print i
            a = loadtxt(i)
            test = loadtxt(i.replace('__best', '__test_best'))
            mm.append(a[:, -1])
            testbest.append(test)

        print len(mm)
        line1 = None
        for m, t in zip(mm, testbest):
            line1, = plt.plot(list(range(1, 31)), m, marker='o',
                              label='Treino')
            line4, = plt.plot(list(range(1, 31)), t, marker='x',
                              label='Teste')

        plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})

        plt.savefig(outfile + '_' + label + '_test.png', dpi=fig.dpi)
        plt.show()
