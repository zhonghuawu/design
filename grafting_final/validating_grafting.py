import numpy as np

import classifying as clf
import grafting as gft
from util import read_data

import sys

def run(fname, fname_test=None, threshold=0.2):
    X, Y= read_data(fname)
    print "run grafting algorithm for data set: %s"%fname
    indexes = gft.grafting(np.matrix(X), np.matrix(Y).T, threshold)[0]
    print "selected features index:"
    print indexes
    print "finish grafting algorithm"
    print "**"*40
    print "run classification:"
    args = {"origin data":np.arange(X.shape[1])}
    args["grafting"] = map(lambda x:int(x), indexes)
    if fname_test==None:
        clf.classifying(X, Y, args=args)
    else:
        X_test, Y_test = read_data(fname_test)
        clf.classifying(X, Y, X_test, Y_test, args=args)
    print "finish classifying"

if __name__ == '__main__':
    fnames = sys.argv[1:]
    if len(fnames) == 1:
        run(fnames[0])
    elif len(fnames) == 2:
        run(fnames[0], fnames[1])
    else :
        print 'arguments error, from %s'%__file__
    print "DONE, end %s"%__file__
