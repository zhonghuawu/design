import scipy.io as sio
import os


def count():
    folder = 'dataset'
    fnames = os.listdir(folder)

    f = open('all_result/all_attribute.csv', 'w')
    info = 'dataset,sample,features,labels\n'
    f.writelines(info)
    for fname in fnames:
        data = sio.loadmat("%s/%s"%(folder, fname))
        n, m = data['X'].shape
        k = len(set(data['Y'][:, 0]))
        info = "%s,%d,%d,%d\n"%(fname.split('.')[0], n, m, k)
        f.writelines(info)
    f.close()

if __name__=='__main__':
    count()

