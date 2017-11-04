#!/usr/bin/env  python


import sys
import numpy as np

filename = sys.argv[1]
ants = int(sys.argv[2])

r = np.loadtxt(filename, delimiter=',')

r /= ants

np.savetxt(filename, r, delimiter=',')
