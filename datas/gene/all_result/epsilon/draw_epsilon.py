# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

def read_output_epsilon(fname):
    res_cls = pd.Series(())
    res_nfs = pd.Series(())
    with open(fname, 'r') as f:
        epsilon = 0.0
        for line in f:
            line_list = line.strip().split(' ')
            if line_list[0] == 'after':
                epsilon = float(line_list[-1][:-1])
            if line_list[0] == 'cross':
                res_cls[epsilon] = float(line_list[-1])
            if line_list[0] == 'size' and line_list[2] == 'data':
                res_nfs[epsilon] = int(line_list[-1][:-1])
    res_cls.name = 'accuracy'
    res_nfs.name = 'compactness'
    return res_cls.drop(0.0), res_nfs.drop(0.0)
    

def draw(cls, nfs, fname):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = ax1.twinx()
    ax1.set_ylabel('Prediction accuracy')
    ax2.set_ylabel('The number of selected features')
    cls.plot(ax=ax1, style='ro-', ylim=(0.0, 1.0), xlim=(0.01, 0.19))
    nfs.plot(ax=ax2, style='g*--', ylim=(0, 150), xlim=(0.01, 0.19))
    plt.xlabel('epsilon')
    ax1.legend(loc="center left")
    ax2.legend(loc="center right")
    fig.suptitle('Effect of epsilon on %s'%fname)

    fig.set_size_inches(9, 6)
    fig.savefig('%s_one.png'%fname, bbox_inches='tight')
    plt.close()

def draw_accuracy(cls, fname):
    fig, ax = plt.subplots(1, 1)
    cls.plot(ax=ax, style='*-', ylim=(0.6, 1.0))
    ax.set_ylabel('Prediction accuracy')
    ax.set_xlabel("epsilon")
    ax.set_title("Prediction accuracy as epsilon changes on dataset %s"%fname)
    plt.show()
    plt.close()

if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    cls, nfs = read_output_epsilon(fname)
    fname = fname.split('.')[0][:-4]
    draw(cls, nfs, fname)
    