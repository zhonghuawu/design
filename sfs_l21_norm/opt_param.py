from grafting_l21 import sfs_l21_norm
from util import read_data
import numpy as np

fname1 = r'../datas/gene/Prostate_GE.mat'
fname2 = r'../datas/gene/ALLAML.mat'

def opt_epsilon(fname, threshold):
    print "dataset: %s"%fname
    X, Y = read_data(fname)
    epsilons = np.arange(0.2, 0.0, -0.01)
    for epsilon in epsilons:
        X_index_retained = sfs_l21_norm(X, Y, threshold, epsilon)[0]
        print "grafting l21-norm ",
        print "threshold = %s, epsilon = %s: "%(str(threshold), str(epsilon)),
        print "%s"%str(list(X_index_retained))

if __name__ == '__main__':
    import sys
    threshold = 0.2
    fname = sys.argv[1]
    opt_epsilon(fname, threshold)
