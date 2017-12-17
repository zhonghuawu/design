# for test some function

import numpy as np

import random

from sklearn import neighbors


# gene n new sample, x is colomn vector
def over_sample_smote(x, n, k):
    minority, _ = x.shape
    new_x = []

    tree = neighbors.KDTree(x)
    for i in range(n):
        # choose x_i randomly
        index = random.choice(range(minority))
        # k-neighbor
        k_neighbor = tree.query(x[index, 0], k)
        print "k_neighbor: {}".format(k_neighbor)
        x_mean = k_neighbor[1].mean()
        print "x_mean: {0}, x_index: {1}".format(x_mean, x[index, 0])
        # gene a new x xigma* (k-neighbor mean)
        new_x_one = x[index, 0] + random.random() * (x_mean - x[index,  0])
        new_x.append(new_x_one)
    new_x = np.matrix(new_x).T
    return new_x

def map_y(y):
    y = list(y)
    y0, y1 = set(y)
    if y.count(y0) < y.count(y1):
        y0, y1 = y1, y0
    y = np.array(y)
    y[y==y0] = 0
    y[y==y1] = 1
    return y

def main():
    # x = np.matrix([random.random() for i in range(9)]).T
    # x = np.matrix(range(9)).T
    # print x
    # print over_sample_smote(x, 5, 6)

    print map_y([1,2,2])


if __name__ == '__main__':
    main()
