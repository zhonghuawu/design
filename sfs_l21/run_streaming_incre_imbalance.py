import sys
import os


def run_one_dataset(ind_fname, dataset_name, threshold, epsilon):
    print "process %s -t %f -e %f" % (dataset_name, threshold, epsilon)
    print "write inds to %s" % ind_fname
    os.system("python streaming_incre.py %s -t %f -e %f > %s" %
              (dataset_name, threshold, epsilon, ind_fname))
    print "finish %s\n" % dataset_name


def main_none():
    dataset_path = "../datas/gene/dataset/"
    ind_path = "../imbalance/ind"

    datasets_name = "colon ALLAML DLBCL".split()

    threshold = 0.2
    epsilon = 0.1
    for dataset_name in datasets_name:
        ind_fname = "%s/%s.ind_imbalance" % (ind_path, dataset_name)
        dataset_name = "%s/%s.mat" % (dataset_path, dataset_name)
        run_one_dataset(ind_fname, dataset_name, threshold, epsilon)

    dataset_name = "GLI_85"
    ind_fname = "%s/%s.ind_imbalance" % (ind_path, dataset_name)
    dataset_name = "%s/%s.mat" % (dataset_path, dataset_name)
    run_one_dataset(ind_fname, dataset_name, threshold, 0.05)


def main_one(fname):
    dataset_path = "../datas/gene/dataset/"
    ind_path = "../imbalance/ind"

    ind_fname = "%s/%s.ind_imbalance" % (ind_path, fname)
    dataset_name = "%s/%s.mat" % (dataset_path, fname)
    threshold = 0.2
    epsilon = 0.1
    run_one_dataset(ind_fname, dataset_name, threshold, epsilon)


def main():
    # main_none()
    fname = sys.argv[1]
    main_one(fname)


if __name__ == '__main__':
    main()
