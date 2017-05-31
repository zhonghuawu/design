import scipy.io as sio
import os

def get_info(fname):
    data = sio.loadmat(fname)
    Y = data['Y'][:, 0]
    labels = set(Y)
    print "%s: %s"%(fname, str(labels))
    labels_dict = {}
    for label in labels:
        labels_dict[label]=0
    for label in Y:
        labels_dict[label]+=1
    for k, v in labels_dict.iteritems():
        print "\tlabel %s: %s"%(k, v)
    print
    return

if __name__=='__main__':
    fnames = os.listdir(r".")
    for fname in fnames:
        if fname.split('.')[-1] == 'mat':
            get_info(fname)
