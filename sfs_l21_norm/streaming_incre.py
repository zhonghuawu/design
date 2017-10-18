from grafting_l21 import sfs_l21_norm_streaming
from util import read_data
import numpy as np
import sys

import time

def sfs(fname, threshold, epsilon):
    # print "dataset: %s"%fname
    X, Y = read_data(fname)

    startTime = time.time()
    sfs_l21_norm_streaming(X, Y, threshold, epsilon)
    endTime = time.time()

    print "%.4f"%(endTime-startTime)

def sfs_part(X, Y, idx, threshold, epsilon):
    X_index_retained = sfs_l21_norm_std(X, Y, idx, threshold, epsilon)[0]
    print "grafting l21-norm ",
    print "threshold = %s, epsilon = %s: "%(str(threshold), str(epsilon)),
    print "%s"%str(list(X_index_retained))

def get_options(args):
    from optparse import OptionParser
    opt = OptionParser(usage='%prog data_file(.mat) [options]')
    opt.add_option('-t', '--threshold', action='store', type='float', dest='threshold', help='coefficient of regularization term(default 0.1)')
    opt.add_option('-e', '--epsilon', action='store', type='float', dest='epsilon', help='value of sample point(default 0.1)')
    opt.set_defaults(threshold=0.2, epsilon=0.05, label_pos=-1)
    return opt.parse_args(args)[0]

if __name__ == '__main__':
    args = sys.argv[1:]
    fname = args[0]
    options = get_options(args)
    sfs(fname, options.threshold, options.epsilon)

