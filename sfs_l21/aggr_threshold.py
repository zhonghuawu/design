import os
import sys

import pandas as pd

def aggr(dataname, epsilon):
    path = r'/home/huaa/design/datas/gene'

    # run grafting_l21
    dataset = r'%s/dataset/%s.mat'%(path, dataname)
    ind_threshold = r'%s/threshold/%s.ind_threshold'%(path, dataname)
    command = r'python opt_threshold.py %s -e %s > %s'%(dataset, epsilon, ind_threshold)
    print "\topt_threshold %s"%dataname
    os.system(command)

    # run classifying
    os.chdir(path)
    output_threshold = r'%s/all_result/threshold/%s_cls.output_threshold'%(path, dataname)
    command = r'python classifying.py %s > %s'%(ind_threshold, output_threshold)
    print "\tclassifying %s"%dataname
    os.system(command)

    # run drawing figure
    # os.chdir("%s/all_result/threshold/"%path)
    # command = r'python draw_threshold.py %s'%output_threshold
    # print "\tdraw_threshold %s"%dataname
    # os.system(command)


if __name__ == '__main__':
    cwd = os.getcwd()
    with open('data_conf', 'r') as f:
            for line in f:
                dataname, threshold, epsilon = line.split()
                print 'process %s'%dataname
                aggr(dataname, epsilon)
                print 'finish %s'%dataname
                os.chdir(cwd)
    # dataname = 'ALLAML'
    # epsilon = 0.2
    # threshold = 0.1
    # aggr(dataname, epsilon, threshold)
