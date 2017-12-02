#!/usr/bin/env python

import numpy as np
from sys import argv


def mean(files, out_file):
    l = [np.loadtxt(f, delimiter=',') for f in files]

    a = np.array(l)

    means = np.mean(a, axis=0)

    np.savetxt(out_file, means)


if __name__ == '__main__':
    files = argv[1:-1]
    outfile = argv[-1]

    mean(files, outfile)
