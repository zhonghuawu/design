import scipy.io as sio

def read_data(fname):
    data = sio.loadmat(fname)
    X = data['X']
    Y = data['Y'][:, 0]
    return X, Y

def main():
    fname = "GLI_85"
    fname = "../datas/gene/dataset/%s.mat" % fname
    X, y = read_data(fname)

if __name__ == '__main__':
    main()
 