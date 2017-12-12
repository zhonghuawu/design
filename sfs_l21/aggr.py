import os
import sys

import pandas as pd

def aggr(dataname, threshold, epsilon):
    path = r'/home/huaa/design/datas/gene'

    # run grafting_l21
    dataset = r'%s/dataset/%s.mat'%(path, dataname)
    ind_streaming_shuffle = r'%s/streaming_shuffle/%s.ind_streaming_shuffle'%(path, dataname)
    command = r'python streaming_incre.py %s -t %s -e %s > %s'%(dataset, threshold, epsilon, ind_streaming_shuffle)
    os.system(command)

    # run classifying
    os.chdir(path)
    output_streaming_shuffle = r'%s/all_result/streaming_shuffle/%s_cls.output_streaming_shuffle'%(path, dataname)
    command = r'python classifying.py %s > %s'%(ind_streaming_shuffle, output_streaming_shuffle)
    os.system(command)

    # run drawing figure
    os.chdir("%s/all_result/streaming_shuffle/"%path)
    command = r'python draw_streaming.py %s'%output_streaming_shuffle
    os.system(command)



if __name__ == '__main__':
    cwd = os.getcwd()
    with open('data_conf', 'r') as f:
            for line in f:
                dataname, threshold, epsilon = line.split()
                print 'process %s'%dataname
                aggr(dataname, threshold, epsilon)
                os.chdir(cwd)
    # dataname = 'ALLAML'
    # epsilon = 0.2
    # threshold = 0.1
    # aggr(dataname, epsilon, threshold)
