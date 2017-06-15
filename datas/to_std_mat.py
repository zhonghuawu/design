#convert *.mat dataset to *.mat with X and Y keys
#X is features
#Y is labels, counted at the begining of 0 to number of categories 

import numpy as np
import scipy.io as sio
import os
import sys

def convert_to_std_mat(fname, label_pos):
    data = sio.loadmat(fname)
    X, y = None, None
    if 'data' in data.keys():
        data = data['data']
        y = data[:, label_pos]
        X = np.delete(data, label_pos, axis=1)
    else :
        X = data['X']
        y = data['Y'][:, 0]
    labels = set(y)
    n, c = len(y), len(labels)
    labels_dict = {}
    for k, label in enumerate(labels):
        labels_dict[label] = k+1
    Y = np.matrix(np.zeros_like(y)).T
    for i, label in enumerate(y):
        Y[i, 0] = labels_dict[label]
    data_dict = {"X":np.matrix(X), "Y":np.matrix(Y).astype(np.int32)}
    sio.savemat("old_gene/%s"%os.path.split(fname)[-1], data_dict)

if __name__ == '__main__':
    fname = sys.argv[1]
    label_pos = sys.argv[2]
    print fname, label_pos
    convert_to_std_mat(fname, int(label_pos))

