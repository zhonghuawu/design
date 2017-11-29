import os
import sys

import pandas as pd

def get_datasets_name():
    datasets_name = []
    with open('dataset/all_attribute.csv', 'r') as f:
        f.readline()
        for line in f:
            if line.startswith('#'):
                continue
            datasets_name.append(line.split(',')[0])
    return datasets_name

def read_output_streaming_cls_nfs_one_dataset(folder, alg):
    res_cls = pd.Series(())
    res_nfs = pd.Series(())
    datasets_name = get_datasets_name()
    for dataset_name in datasets_name:
        if alg == "Alpha_investing" and dataset_name == "DLBCL":
             continue
        with open("%s/streaming_%s/%s_cls.output_streaming"%(folder, alg, dataset_name), 'r') as f:
            for line in f:
                line_list = line.split()
                if line_list[0]=='size' and line_list[2] == 'data':
                    res_nfs[dataset_name] = long(line_list[-1][:-1])
                if line_list[0]=='cross':
                    res_cls[dataset_name] = float(line_list[-1])
    res_cls.name = alg
    res_nfs.name = alg
    return res_cls, res_nfs
    

def main(folder):
    alg = 'l21'
    cls, nfs= read_output_streaming_cls_nfs_one_dataset(folder, alg)
    cls.name = "sfs_l21"
    nfs.name = "sfs_l21"

    algs = 'grafting osfs Alpha_investing saola'
    for alg in algs.split():
        cls_tmp, nfs_tmp = read_output_streaming_cls_nfs_one_dataset(folder, alg)
        cls = pd.concat((cls, cls_tmp), axis=1)
        nfs = pd.concat((nfs, nfs_tmp), axis=1)
    cls.to_csv("%s/all_cls.csv"%folder)
    nfs.to_csv("%s/all_nfs.csv"%folder)
    print cls
    print nfs

if __name__ == '__main__':
    folder = sys.argv[1]
    main(folder)
