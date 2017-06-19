from grafting_l21 import sfs_l21_norm
from util import read_data
import numpy as np

def opt_threshold(fname, epsilon):
    print "datasets: %s"%fname
    X, Y = read_data(fname)
    thresholds = np.arange(0.1, 1.0, 0.1)
    for threshold in thresholds:
        X_index_retained = sfs_l21_norm(X, Y, threshold, epsilon)[0]
        print "grafting l21-norm ",
        print "threshold = %s, epsilon = %s: "%(str(threshold), str(epsilon)),
        print "%s"%str(list(X_index_retained))

if __name__ == '__main__':
    import sys
    epsilon = 0.1
    fname = sys.argv[1]
    opt_threshold(fname, epsilon)
