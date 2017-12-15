'''
streaming feature selection regularized by l21-norm
X: data matrix, n*d dimension
Y: label matrix, n*c dimension
W: selection matrix, d*c
threshold: scalar, 0.1-0.5 empirical value
here,
n is number of samples
d is number of features
c is categories of labels
'''

"""
 feature selection for two-class imbalance dataset
"""

import numpy as np
import matplotlib.pyplot as plt

import random

from model import *
from util import read_data

import time


from sklearn import neighbors

# random downsampling
def under_sampling_random(y):
    zeros = [i for i, a in enumerate(y) if a == 0]
    ones = [i for i, a in enumerate(y) if a == 1]
    minority = min(len(zeros), len(ones))
    selected_samlpe = []
    if minority == len(ones):  # label 1 is minority class
        selected_samlpe = ones
        random.shuffle(zeros)
        selected_samlpe.extend(zeros[:minority])
    else:  # label 0 is minority class
        selected_samlpe = zeros
        random.shuffle(ones)
        selected_samlpe.extend(ones[:minority])
    selected_samlpe.sort()
    return selected_samlpe


# over sample using smote algorithm
# generate n new sample based on x
# rare is len(x)
def over_sample_smote(x, n, k):
    minority, _ = x.shape
    new_x = []

    tree = neighbors.KDTree(x)
    for i in range(n):
        # choose x_i randomly
        index = random.choice(range(minority))
        # k-neighbor
        x_mean = tree.query(x[index, 0], k)[0].mean()
        # gene a new x xigma* (k-neighbor mean)
        new_x_one = x[index, 0] + random.random() * x_mean
        new_x.append(new_x_one)
    new_x = np.matrix(new_x).T
    return new_x


def sfs_l21_norm(X, Y, threshold, epsilon):
    X, Y = np.matrix(X), np.matrix(Y)

    y = list(Y[:, 1])
    zeros = [i for i, a in enumerate(y) if a == 0]
    ones = [i for i, a in enumerate(y) if a == 1]
    minority = min(len(zeros), len(ones))
    majority = max(len(zeros), len(ones))
    k = majority - minority  # generate k new sample
    minority_samlpe_index = None
    Y_new = None
    zeros_k = np.matrix(np.zeros(k)).T
    ones_k = np.matrix(np.ones(k)).T
    if minority == len(zeros):  # label 0 is minority class
        minority_samlpe_index = zeros
        Y_new = np.hstack((ones_k, zeros_k))
    else:  # label 1 is minority class
        minority_samlpe_index = ones
        Y_new = np.hstack((zeros_k, ones_k))

    Y = np.vstack((Y, Y_new))
    X_model = np.ones_like(Y[:, 0])
    W = np.ones_like(Y[0, :])
    W, obj_value = update_weight(W, X_model, Y, threshold)

    X_index = np.array((), dtype=int)
    X_index_retained = np.array((), dtype=int)
    obj_values = np.array((), dtype=float)

    n, d = X.shape
    n, c = Y.shape
    print X.shape, Y.shape
    print "minority_samlpe_index sample: ", minority_samlpe_index

    for j in range(d):
        x_new = over_sample_smote(X[minority_samlpe_index, j], k, 5)
        x = np.vstack((X[:, j], x_new))
        if gradient_validation(x, W, X_model, Y, threshold, epsilon):
            X_index_retained = np.hstack((X_index_retained, j))
            X_model = np.hstack((X_model, x))
            W = np.vstack((W, np.ones(c)))
            W, obj_value = update_weight(W, X_model, Y, threshold)
            W, X_model, X_index_retained = refresh_selected(
                W, X_model, X_index_retained)
            X_index = np.hstack((X_index, j))
            obj_values = np.hstack((obj_values, obj_value))
    return X_index_retained, W, X_index, obj_values


def sfs_l21_norm_streaming(X, Y, threshold, epsilon):
    X, Y = np.matrix(X), np.matrix(Y)

    y = list(Y[:, 1])
    zeros = [i for i, a in enumerate(y) if a == 0]
    ones = [i for i, a in enumerate(y) if a == 1]
    minority = min(len(zeros), len(ones))
    majority = max(len(zeros), len(ones))
    k = majority - minority  # generate k new sample
    minority_samlpe_index = None
    Y_new = None
    zeros_k = np.matrix(np.zeros(k)).T
    ones_k = np.matrix(np.ones(k)).T
    if minority == len(zeros):  # label 0 is minority class
        minority_samlpe_index = zeros
        Y_new = np.hstack((ones_k, zeros_k))
    else:  # label 1 is minority class
        minority_samlpe_index = ones
        Y_new = np.hstack((zeros_k, ones_k))

    Y = np.vstack((Y, Y_new))
    X_model = np.ones_like(Y[:, 0])
    W = np.ones_like(Y[0, :])
    W, obj_value = update_weight(W, X_model, Y, threshold)

    X_index = np.array((), dtype=int)
    X_index_retained = np.array((), dtype=int)
    obj_values = np.array((), dtype=float)

    n, d = X.shape
    n, c = Y.shape

    d_part = (d + 9) / 10
    idx = np.arange(d)

    for j in range(d):
        x_new = over_sample_smote(X[minority_samlpe_index, j], k, 5)
        x = np.vstack((X[:, j], x_new))
        x = normalizate(x)
        if gradient_validation(x, W, X_model, Y, threshold, epsilon):
            X_index_retained = np.hstack((X_index_retained, j))
            X_model = np.hstack((X_model, x))
            W = np.vstack((W, np.ones(c)))
            W, obj_value = update_weight(W, X_model, Y, threshold)
            W, X_model, X_index_retained = refresh_selected(
                W, X_model, X_index_retained)
            X_index = np.hstack((X_index, j))
            obj_values = np.hstack((obj_values, obj_value))
        if not (j + 1) % d_part:
            print "%2d0%% " % ((j + 1) / d_part),
            print "sfs l21-norm ",
            print "threshold = %s, epsilon = %s: " % (str(threshold), str(epsilon)),
            print "%s" % str(list(X_index_retained))
    print "100% ",
    print "sfs l21-norm ",
    print "threshold = %s, epsilon = %s: " % (str(threshold), str(epsilon)),
    print "%s" % str(list(X_index_retained))
    return X_index_retained, W, X_index, obj_values


def main(fname, threshold, epsilon):
    X, Y = read_data(fname)
    print X.shape, Y.shape
    print "X shape: %s" % str(X.shape)

    startTime = time.time()
    X_index_retained, W, X_index, obj_values = sfs_l21_norm(
        X, Y, threshold, epsilon)
    endTime = time.time()

    print "runtime: %.4f seconds" % (endTime - startTime)

    print "**" * 30
    print "data set name: %s" % fname
    print "selected features index: "
    print "sfs-l21-norm "
    print "threshold = %s, epsilon = %s: " % (str(threshold), str(epsilon)),
    print "%s\n" % str(list(X_index_retained))
    print "selected features weight: \n%s\n" % str(W)
    print "features index that through the gradient validation: \n%s\n" % str(X_index)
    print "**" * 30
    print "DONE"

    obj_values_df = pd.DataFrame(
        obj_values, index=X_index, columns=["obj_values"])
    columns = ["weight_%d" % i for i in range(Y.shape[1])]
    weights_df = pd.DataFrame(W, index=np.hstack(
        (-1, X_index_retained)), columns=columns)
    df = pd.concat((obj_values_df, weights_df))
    df.plot(subplots=True)
    plt.show()


def get_options(args):
    from optparse import OptionParser
    opt = OptionParser(usage='%prog data_file(.mat) [options]')
    opt.add_option('-t', '--threshold', action='store', type='float',
                   dest='threshold', help='coefficient of regularization term(default 0.1)')
    opt.add_option('-e', '--epsilon', action='store', type='float',
                   dest='epsilon', help='value of sample point(default 0.1)')
    opt.set_defaults(threshold=0.2, epsilon=0.1, label_pos=-1)
    return opt.parse_args(args)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    fname = args[0]
    options, args = get_options(args[1:])
    run(fname, options.threshold, options.epsilon)
