import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras import optimizers


class NeuralNetwork(object):
    def __init__(self, neurons, epochs, batch_size, hidden_layers,
                 learning_rate, lr_decay=False, seed=None, stats=None):
        self.neurons = neurons
        self.epochs = epochs
        self.batch_size = batch_size
        self.hidden_layers = hidden_layers
        self.learning_rate = learning_rate
        self.lr_decay = lr_decay
        self.stats = stats
        np.random.seed(seed)

    def __dump_to_file(self, scores_keys, scores, histories):
        base = self.stats + '__'

        d_scores = {k: [] for k in scores_keys}
        for k, s in zip(scores_keys, scores):
            d_scores[k].append(s)

        for k, v in d_scores.items():
            outfile = base + 'test' + '_' + k + '.csv'
            np.savetxt(outfile, v, delimiter=',')

        d_hist = {k: [] for k in histories[0].keys()}
        for history in histories:
            for k, v in history.items():
                d_hist[k].append(v)

        for k, v in d_hist.items():
            outfile = base + 'history' + '_' + k + '.csv'
            np.savetxt(outfile, v, delimiter=',')

    def create_model(self):
        model = Sequential()
        model.add(Dense(self.neurons,
                        input_dim=self.initial,
                        activation='sigmoid'))

        for i in range(self.hidden_layers - 1):
            model.add(Dense(self.neurons, activation='sigmoid'))

        model.add(Dense(self.final, activation='sigmoid'))

        if self.lr_decay is None:
            opt = optimizers.SGD(self.learning_rate)
        else:
            opt = optimizers.SGD(lr=self.learning_rate, decay=self.lr_decay)

        # Compile model
        model.compile(loss='categorical_crossentropy',
                      optimizer=opt,
                      metrics=['accuracy'])
        return model

    # encode class values as integers
    def encode(self, Y, nclasses=False):
        y_set = sorted(set(Y))

        labels = {y: i for i, y in enumerate(y_set)}

        encoded_Y = np.array([labels[y] for y in Y])

        return len(y_set), encoded_Y if nclasses else encoded_Y

    def k_fold(self, data, k=3, shuffle=False):
        if shuffle:
            np.random.shuffle(data)

        chunks = np.array_split(data, k)

        for cur_k in range(k):
            training = np.concatenate(
                [x for i, x in enumerate(chunks) if i != cur_k])
            validation = chunks[cur_k]
            yield training, validation

    def k_fold_cross_validation(self, X, Y, k):
        indices = np.arange(len(X))
        kfold = self.k_fold(indices, k=k, shuffle=True)

        results = []
        histories = []

        for i, (train, test) in enumerate(kfold):
            print("Running Fold", i + 1, "/", k)
            model = None    # Clearing the NN.
            model = self.create_model()

            history = model.fit(X[train], Y[train],
                                epochs=self.epochs,
                                batch_size=self.batch_size)

            # evaluate the model
            scores = model.evaluate(X[test], Y[test])
            print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

            histories.append(history.history)
            results.append(scores[1] * 100)

        self.__dump_to_file(model.metrics_names, results, histories)

        return results

    def run(self, X, Y):
        self.initial = X.shape[1]
        self.final, encoded_Y = self.encode(Y, nclasses=True)

        # convert integers to dummy variables (i.e. one hot encoded)
        dummy_y = np_utils.to_categorical(encoded_Y)

        results = self.k_fold_cross_validation(X, dummy_y, 3)
        print("%.2f%% (+/- %.2f%%)" % (np.mean(results), np.std(results)))

        return
