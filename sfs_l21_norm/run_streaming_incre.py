import sys
import os

dataset_type = 'text'
# dataset_type = 'faceImage'

def get_datasets_name():
    fname='../datas/%s/all_result/all_attribute.csv'%dataset_type
    datasets_name = []
    with open(fname, 'r') as f:
        f.readline()
        for line in f:
            dataset_name = line.split(',')[0]
            datasets_name.append(dataset_name)
    return datasets_name

def main():
    datasets_name = get_datasets_name()
    # datasets_name = "ORL Yale".split()
    path=r'../datas/%s'%dataset_type

    threshold = 0.2
    epsilon = 0.02
    for dataset_name in datasets_name:
        dataset_fname = "%s/dataset/%s.mat"%(path, dataset_name)
        ind_fname = "%s/ind_streaming_l21/%s.ind_streaming_l21"%(path, dataset_name)
        print "process %s"%dataset_name
        os.system("python streaming_incre.py %s -t %f -e %f > %s"%(dataset_fname, threshold, epsilon, ind_fname))
        print "finish %s"%dataset_name

if __name__ == '__main__':
    main()

