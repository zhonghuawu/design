#convert pure text datas to mat format for octave

import pandas as pd
from pandas import DataFrame
import scipy.io as sio
import numpy as np

import sys

def convert_to_mat(filename, nullvalue='?', separater=',', hd=None):
    df = pd.read_csv(filename, sep=separater, header=hd)
    labels=df.get_values()[:, -1]
    categories=set(labels)
    cates_dict={}
    for k, category in enumerate(categories):
        cates_dict[category]=k
    for k, label in enumerate(labels):
        labels[k] = cates_dict[label]
    df = df.drop(len(df.columns)-1, axis=1)
    df = df.replace([nullvalue], np.NaN)
    df = df.astype(np.float)
    #for k, data in enumerate(df):
    #    df[k]=df[k].fillna(data.mean())
    for col in df.columns:
        df[col] = df[col].fillna(df[col].mean())
    labels = DataFrame(labels, columns=[len(df.columns)])
    df = pd.concat([df, labels], axis=1)
    values = df.get_values()
    values = np.array(values, dtype=np.float)
    mat_name = filename.split('.')[0]
    #array_name = mat_name.split('/')[-1]
    sio.savemat('%s.mat'%mat_name, {"data" : values})

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        data_file_name = sys.argv[i]
        print "start to convert: %s"%data_file_name
        convert_to_mat(data_file_name)
        print "finish: %s"%data_file_name

