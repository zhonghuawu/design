# for test some function

import numpy as np
from numpy import matrix

import random

def over_sample_smote(x, k, rare):
    new_x = []
    for i in range(k):
        index = random.choice(range(rare))  # choose x_i randomly
        x_x = x - x[index, 0]
        x_x.sort()
        print "x_x: ", x_x
        x_x_k = x_x[:k, 0]
        new_x_one = random.random() * x_x_k.mean()
        new_x.append(new_x_one)
    new_x = np.matrix(new_x).T
    return new_x


def main():
    x = matrix([random.random() for i in range(9)]).T
    print x
    print over_sample_smote(x, 5, 9)
    
    

if __name__ == '__main__':
    main()
