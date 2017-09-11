import pandas as pd
import os

def get_datasets_name():
    datasets_name = []
    with open('all_attribute.csv', 'r') as f:
        f.readline()
        for line in f:
            datasets_name.append(line.split(',')[0])
    return datasets_name

def read_output_streaming_cls_nfs_one_dataset(alg):
    res_cls = pd.Series(())
    res_nfs = pd.Series(())
    datasets_name = get_datasets_name()
    for dataset_name in datasets_name:
        with open("%s/%s_cls.output_%s"%(alg, dataset_name, alg), 'r') as f:
            for line in f:
                line_list = line.split()
                if line_list[0]=='size' and line_list[2] == 'data':
                    res_nfs[dataset_name] = int(line_list[-1][:-1])
                if line_list[0]=='cross':
                    res_cls[dataset_name] = float(line_list[-1])
    res_cls.name = alg
    res_nfs.name = alg
    return res_cls, res_nfs
    

def main():
    # datasets_name = get_datasets_name()
    alg = 'streaming_grafting'
    cls_grafting, nfs_grafting = read_output_streaming_cls_nfs_one_dataset(alg)

    alg = 'streaming_l21'
    cls_l21, nfs_l21 = read_output_streaming_cls_nfs_one_dataset(alg)

    cls = pd.concat((cls_l21, cls_grafting), axis = 1)
    nfs = pd.concat((nfs_l21, nfs_grafting), axis = 1)
    print cls
    print nfs

if __name__ == '__main__':
    main()
