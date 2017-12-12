from sfs_l21 import sfs_l21_norm
from util import read_data
import numpy as np

import sys

def opt_epsilon(fname, threshold):
    # print "dataset: %s"%fname
    X, Y = read_data(fname)
    # epsilons = np.arange(0.2, 0.0, -0.01)
    epsilons = np.arange(0.01, 0.2, 0.02)
    for epsilon in epsilons:
        X_index_retained = sfs_l21_norm(X, Y, threshold, epsilon)[0]
        print "grafting l21-norm ",
        print "threshold = %s, epsilon = %s: "%(str(threshold), str(epsilon)),
        print "%s"%str(list(X_index_retained))

def get_options(args):
    from optparse import OptionParser
    opt = OptionParser(usage='%prog data_file(.mat) [options]')
    opt.add_option('-t', '--threshold', action='store', type='float', dest='threshold', help='coefficient of regularization term(default 0.1)')
    opt.set_defaults(threshold=0.2)
    return opt.parse_args(args)[0]

if __name__ == '__main__':
    # threshold = 0.2
    args = sys.argv[1:]
    fname = args[0]
    options = get_options(args)
    opt_epsilon(fname, options.threshold)
