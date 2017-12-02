#!/usr/bin/env python3

import numpy as np
import argparse
from neuralnetwork import NeuralNetwork


# load dataset
def load_dataset(filename, delimiter=','):
    dataset = np.loadtxt(filename, dtype=object, delimiter=delimiter)
    X = (dataset[:, 0:-1]).astype(float)
    Y = dataset[:, -1]
    return X, Y


def main(args):
    filename = args.file
    neurons = args.neurons
    epochs = args.epochs
    batch_size = args.batch_size
    hidden_layers = args.hidden_layers
    learning_rate = args.learning_rate
    lr_decay = args.lr_decay
    seed = args.seed
    stats = args.stats

    X, Y = load_dataset(filename, delimiter=';')

    net = NeuralNetwork(neurons, epochs, batch_size, hidden_layers,
                        learning_rate, lr_decay, seed, stats)
    net.run(X, Y)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True,
                        help='Input file.')
    parser.add_argument('-n', '--neurons', type=int, default=8,
                        help='Number of neurons on each hidden layer.')
    parser.add_argument('-hl', '--hidden_layers', type=int, default=1,
                        help='Number of hidden layers.')
    parser.add_argument('-e', '--epochs', type=int, default=100,
                        help='Number of epochs.')
    parser.add_argument('-lr', '--learning_rate', type=float, default=3,
                        help='Learning rate.')
    parser.add_argument('-b', '--batch_size', type=int, default=32,
                        help='Size of mini-batch.')
    parser.add_argument('-d', '--lr_decay', type=float, default=0.0,
                        help='Decay rate of the learning rate.')
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help='Seed for random number generator.')
    parser.add_argument('--stats', default='',
                        help='File to save statistics.')

    args = parser.parse_args()
    print(args)
    main(args)
