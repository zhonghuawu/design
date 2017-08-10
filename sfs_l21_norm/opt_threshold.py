from grafting_l21 import sfs_l21_norm
from util import read_data
import numpy as np

import sys

def opt_threshold(fname, epsilon):
    # print "datasets: %s"%fname
    X, Y = read_data(fname)
    thresholds = np.arange(0.1, 0.51, 0.05)
    for threshold in thresholds:
        X_index_retained = sfs_l21_norm(X, Y, threshold, epsilon)[0]
        print "grafting l21-norm ",
        print "threshold = %s, epsilon = %s: "%(str(threshold), str(epsilon)),
        print "%s"%str(list(X_index_retained))

def get_options(args):
    from optparse import OptionParser
    opt = OptionParser(usage='%prog data_file(.mat) [options]')
    opt.add_option('-e', '--epsilon', action='store', type='float', dest='epsilon', help='value of sample point(default 0.1)')
    opt.set_defaults(threshold=0.2, epsilon=0.05, label_pos=-1)
    return opt.parse_args(args)[0]

if __name__ == '__main__':
    # epsilon = 0.05
    args = sys.argv[1:]
    fname = args[0]
    options = get_options(args)
    opt_threshold(fname, options.epsilon)
