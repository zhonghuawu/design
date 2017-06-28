from grafting_l21 import sfs_l21_norm_streaming
from util import read_data
import numpy as np
import sys

def sfs(fname, threshold, epsilon):
    print "dataset: %s"%fname
    X, Y = read_data(fname)
    sfs_l21_norm_streaming(X, Y, threshold, epsilon)

def sfs_part(X, Y, idx, threshold, epsilon):
    X_index_retained = sfs_l21_norm_std(X, Y, idx, threshold, epsilon)[0]
    print "grafting l21-norm ",
    print "threshold = %s, epsilon = %s: "%(str(threshold), str(epsilon)),
    print "%s"%str(list(X_index_retained))

if __name__ == '__main__':
    threshold = 0.2
    epsilon = 0.1
    fname = sys.argv[1]
    sfs(fname, threshold, epsilon)


