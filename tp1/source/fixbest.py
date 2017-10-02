import numpy as np
from sys import argv


def fix(input_file, output_file):

    a = np.loadtxt(input_file, delimiter=',')

    for i in range(a.shape[0]):
        for j in range(1,a.shape[1]):
            a[i][j] = min(a[i][j],a[i][j-1])

    np.savetxt(output_file, a, delimiter=',')

input_file = argv[1]

if len(argv) < 3:
    output_file = input_file
else:
    output_file = argv[2]

fix(input_file, output_file)