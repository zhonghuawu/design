import scipy.io as sio
import numpy as np

def read_data(fname):
    data = sio.loadmat(fname)['data']
    X = data[:, :-1]
    y = data[:, -1]
    numberOfClasses=len(set(y))
    numberOfSamples=len(y)
    Y = np.matrix(np.zeros((numberOfSamples, numberOfClasses)))
    for i in range(numberOfSamples):
        Y[i, int(y[i])] = 1
    return np.matrix(X), np.matrix(Y)

def Loss_fro(W, X, Y):
    mat = np.dot(X, W)-Y
    return np.linalg.norm(mat, ord='fro')

def Regularized_term(W):
    vec = np.linalg.norm(W, ord=2, axis=1)
    return np.linalg.norm(vec, ord=1, axis=0)

def F(W, X, Y, threshold):
    W = np.matrix(W).reshape((X.shape[1], Y.shape[1]))
    return Loss_fro(W, X, Y)+threshold*Regularized_term(W)

def fprime(xk, f, epsilon, *args):
    f0 = f(*((xk,)+args))
    grad = np.zeros((xk.shape), float)
    ei = np.zeros((xk.shape), float)
    for i in range(xk.shape[0]):
        for j in range(xk.shape[1]):
            ei[i, j] = 1.0
            d = np.multiply(epsilon, ei)
            grad[i, j] = (f(*((xk+d,)+args))-f0)/d[i, j]
            ei[i, j] = 0.0
    return grad

if __name__ == "__main__":
    fname="../datas/DLBCL-Stanford/DLBCL-Stanford.mat"
    fname="../datas/ColonTumor/colonTumor.mat"
    print fname
    X, Y = read_data(fname)
    X_index = np.array((1,2,4,5))
    X_model = X[:, X_index]
    d, c = X_model.shape[1], Y.shape[1]
    W = np.ones((d, c))
    from scipy import optimize as opt
    threshold = 0.01
    W = opt.fmin_cg(F, W, args=(X_model, Y, threshold)).reshape((d, c))
    W = np.matrix(W)
    print "W = %s"%str(W)
    eps = np.sqrt(np.finfo(float).eps)
    eps_mat = eps*W
    w_prime = fprime(W, F, eps_mat, X_model, Y, threshold)
    print "w_prime = %s"%str(w_prime)
