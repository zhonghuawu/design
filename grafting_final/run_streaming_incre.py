import sys
import os

def get_datasets_name():
    fname='../datas/gene/all_result/all_attribute.csv'
    datasets_name = []
    with open(fname, 'r') as f:
        f.readline()
        for line in f:
            dataset_name = line.split(',')[0]
            datasets_name.append(dataset_name)
    return datasets_name

def main():
    datasets_name = get_datasets_name()
    path=r'../datas/gene'

    threshold = 0.2
    epsilon = 0.1
    for dataset_name in datasets_name:
        dataset_fname = "%s/dataset/%s.mat"%(path, dataset_name)
        ind_fname = "%s/streaming_grafting/%s.ind_streaming_grafting"%(path, dataset_name)
        print "process %s"%dataset_name
        os.system("python streaming_incre.py %s > %s"%(dataset_fname, ind_fname))
        print "finish %s"%dataset_name

if __name__ == '__main__':
    main()

