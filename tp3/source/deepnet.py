#!/usr/bin/env python3

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils


# fix random seed for reproducibility
seed = None
np.random.seed(seed)


# load dataset
def load_dataset(filename, delimiter=','):
    dataset = np.loadtxt(filename, dtype=object, delimiter=delimiter)
    X = (dataset[:, 0:-1]).astype(float)
    Y = dataset[:, -1]
    return X, Y


# encode class values as integers
def encode(Y, y_set=[], nclasses=False):
    if not y_set:
        y_set = sorted(list(set(Y)))

    labels = {}
    for i, y in enumerate(y_set):
        labels[y] = i

    encoded_Y = np.empty(len(Y), dtype=int)
    for i, y in enumerate(Y):
        encoded_Y[i] = labels[y]

    return len(y_set), encoded_Y if nclasses else encoded_Y


def main(filename):
    X, Y = load_dataset(filename, delimiter=';')
    initial = X.shape[1]
    neurons = initial * 2

    final, encoded_Y = encode(Y, nclasses=True)

    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_Y)

    model = Sequential()
    model.add(Dense(neurons, input_dim=initial, activation='sigmoid'))
    model.add(Dense(final, activation='softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    history = model.fit(X, dummy_y, validation_split=0.3, epochs=500)


if __name__ == '__main__':
    filename = '../dataset/yeast_modified.csv'
    main(filename)
