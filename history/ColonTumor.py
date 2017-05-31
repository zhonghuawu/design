import pandas as pd
from pandas import DataFrame, Series
from sklearn import svm
from sklearn import datasets
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score

import numpy
import scipy

def run(X, y):
    print X.shape, y.shape
    #clf = svm.SVC()
    clf = svm.LinearSVC()
    scores = cross_validation.cross_val_score(clf, X, y, cv=6, scoring="accuracy")
    print "scores: ", scores, scores.mean()
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    print cm
    print "y_test = ", y_test
    print "y_pred = ", y_pred
    print "MCC: %f"%matthews_corrcoef(y_test, y_pred)
    print "ACC: %f"%accuracy_score(y_test, y_pred)

def run_all(X, y):
    print X.shape, y.shape
    clf = svm.SVC()
    #clf = svm.LinearSVC()
    scores = cross_validation.cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    print "scores: ", scores, scores.mean()
    clf.fit(X, y)
    y_pred = clf.predict(X)

    cm = confusion_matrix(y, y_pred)
    print cm
    print "y_test = ", y
    print "y_pred = ", y_pred
    print "MCC: %f"%matthews_corrcoef(y, y_pred)
    print "ACC: %f"%accuracy_score(y, y_pred)

if __name__ == "__main__":
    fr_n = r"/home/huaa/workspace/datas/gene_expr/ColonTumor/colonTumor.data"
    datas = pd.read_csv(fr_n, sep=',', header=None)
    n_features = len(datas.columns)
    yy = datas[n_features-1]
    X = datas.drop(n_features-1, axis=1).get_values()
    y = [0 if i==yy[0] else 1 for i in yy]
    X, y = numpy.array(X), numpy.array(y)
    print "origion datas:"
    #run(X, y)
    run_all(X, y)
    #index = [2, 8, 10, 13, 14, 22, 25, 42, 48, 61, 65, 71, 74, 110, 137, 186, 244, 248, 265, 364, 376, 390, 426, 492, 526, 600, 624, 697, 764, 801, 978, 1023, 1046, 1059, 1152, 1324, 1345, 1369, 1422, 1465, 1472, 1581, 1607, 1770, 1771, 1774, 1869]
    #index = [1974, 1993]
    #index = [14, 193]
    index = [80, 72, 943,  168,  157 , 162,  312 ,  82 ,1340 ,1721 ,1227 ,1692 ,1289 ,1711 , 431, 1508 ,1997 ,1974 ,1988 ,1980 ,1998 ,1950 ,1990 ,1994 ,1985]
    X = X[:, index]
    print "after features selection:"
    #run(X, y)
    run_all(X, y)
    print "Done!"
