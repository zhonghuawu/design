import os
import sys

import pandas as pd

def aggr(dataname, threshold):
    path = r'/home/huaa/design/datas/gene'

    # run grafting_l21
    dataset = r'%s/dataset/%s.mat'%(path, dataname)
    ind_epsilon = r'%s/epsilon/%s.ind_epsilon'%(path, dataname)
    command = r'python opt_epsilon.py %s -t %s > %s'%(dataset, threshold, ind_epsilon)
    print "\topt_epsilon %s"%dataname
    os.system(command)

    # run classifying
    os.chdir(path)
    output_epsilon = r'%s/all_result/epsilon/%s_cls.output_epsilon'%(path, dataname)
    command = r'python classifying.py %s > %s'%(ind_epsilon, output_epsilon)
    print "\tclassifying %s"%dataname
    os.system(command)

    # run drawing figure
    os.chdir("%s/all_result/epsilon/"%path)
    command = r'python draw_epsilon.py %s'%output_epsilon
    print "\tdraw_epsilon %s"%dataname
    os.system(command)


if __name__ == '__main__':
    cwd = os.getcwd()
    with open('data_conf', 'r') as f:
            for line in f:
                dataname, threshold, epsilon = line.split()
                print 'process %s'%dataname
                aggr(dataname, threshold)
                print 'finish %s\n'%dataname
                os.chdir(cwd)
    # dataname = 'ALLAML'
    # epsilon = 0.2
    # threshold = 0.1
    # aggr(dataname, epsilon, threshold)
