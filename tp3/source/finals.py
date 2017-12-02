#!/usr/bin/env python

import numpy as np
from sys import argv


def final(file, out_file):
    l = np.loadtxt(file)

    a = np.array(l)

    finals = a[:, -1]
    # print(finals)

    np.savetxt(out_file, finals)


if __name__ == '__main__':
    file = argv[1]
    outfile = argv[2]

    final(file, outfile)
