import pandas as pd
from pandas import DataFrame, Series
from sklearn import svm


from sklearn.metrics import confusion_matrix
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import accuracy_score

import numpy

def run(X_train, y_train, X_test, y_test):
    print X_train.shape, y_train.shape
    clf = svm.LinearSVC()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    print cm
    print "MCC: %f"%matthews_corrcoef(y_test, y_pred)
    print "ACC: %f"%accuracy_score(y_test, y_pred)

def read_Leukemia(fr_n):
    datas = pd.read_csv(fr_n, sep=',', header=None)
    n_features = len(datas.columns)
    yy = datas[n_features-1]
    X = datas.drop(n_features-1, axis=1).get_values()
    y = [0 if i==yy[0] else 1 for i in yy]
    X, y = numpy.array(X), numpy.array(y)
    return X, y

if __name__ == "__main__":
    ftrain = r"/home/huaa/workspace/datas/gene_expr/Leukemia/AMLALL_train.data"
    ftest = r"/home/huaa/workspace/datas/gene_expr/Leukemia/AMLALL_test.data"
    X_train, y_train = read_Leukemia(ftrain)
    X_test, y_test = read_Leukemia(ftest)
    print "origion datas:"
    run(X_train, y_train, X_test, y_test)
    #index = [0, 156, 172, 247, 311, 460, 963, 1246, 1248, 1305, 1744, 1778, 1795, 1806, 1833, 1852, 1881, 1940, 2019, 2110, 2118, 2241, 2266, 2287, 2348, 2401, 3319, 3773, 3846, 3897, 4051, 4185, 4498, 4846, 4950, 5001, 5038, 5597, 5765, 5953, 6168, 6404, 6431, 6538]
    index = [44, 45, 72, 472, 1520, 6470, 1491, 1705, 5542, 6471, 4515, 6167, 6063, 3837, 124, 1694, 3695, 1485, 6377, 6752, 5649, 6782, 7081, 7124, 7086]

    X_train = X_train[:, index]
    X_test = X_test[:, index]
    print "after features selection:"
    run(X_train, y_train, X_test, y_test)
    print "Done!"
