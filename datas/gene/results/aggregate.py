import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def read_output(fname):
    res_cls = pd.Series(())
    res_nfs = pd.Series(())
    with open(fname, 'r') as f:
        line = f.readline()
        dataset_name = line.split('/')[-1].strip()
        res_cls.name = "%s_cls"%dataset_name
        res_nfs.name = "%s_nfs"%dataset_name
        f.readline()
        alg_name = 'origin data: '
        for line in f:
            line_list = line.strip().split(' ')
            if line_list[0] == 'after':
                alg_name = line.strip()[15:]
                if alg_name.startswith("grafting"):
                    alg_name = alg_name[9:]
            if line_list[0] == 'cross':
                res_cls[alg_name] = float(line_list[-1])
            if line_list[0] == 'size' and line_list[2] == 'data':
                res_nfs[alg_name] = int(line_list[-1][:-1])
    res = pd.concat([res_cls, res_nfs], axis=1)
    return res

def read_all(fnames):
    f = open('all.txt','wa')
    for fname in fnames:
        if fname.endswith('output'):
            res = read_output(fname)
            f.write(str(res))
            f.write('\n\n')
    f.close()

if __name__ == '__main__':
    path = os.getcwd()
    fnames = os.listdir(path)
    read_all(fnames[0:])
