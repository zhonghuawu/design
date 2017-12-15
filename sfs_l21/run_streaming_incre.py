import sys
import os

dataset_type = 'gene'
# dataset_type = 'faceImage'
# dataset_type = 'text'
# dataset_type = 'other'


def get_datasets_name():
    fname='../datas/%s/dataset/all_attribute.csv'%dataset_type
    datasets_name = []
    with open(fname, 'r') as f:
        f.readline()
        for line in f:
            dataset_name = line.split(',')[0]
            datasets_name.append(dataset_name)
    return datasets_name

def run_one_dataset(path, dataset_name, threshold, epsilon):
    dataset_fname = "%s/dataset/%s.mat"%(path, dataset_name)
    ind_fname = "%s/ind_streaming_imbalance/%s.ind_imbalance"%(path, dataset_name)
    print "process %s"%dataset_name
    print "write inds to %s"%ind_fname
    os.system("python streaming_incre.py %s -t %f -e %f > %s"%(dataset_fname, threshold, epsilon, ind_fname))
    print "finish %s"%dataset_name


def main():
    # datasets_name = get_datasets_name()
    datasets_name = "colon ALLAML DLBCL".split()
    path=r'../datas/%s'%dataset_type

    threshold = 0.2
    epsilon = 0.1
    for dataset_name in datasets_name:
        run_one_dataset(path, dataset_name, threshold, epsilon)

    run_one_dataset(path, "GLI_85", threshold, 0.05)
if __name__ == '__main__':
    main()

