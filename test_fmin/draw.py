import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

#X = np.matrix(np.random.random((3,10)))
X = np.matrix(
        [[0.61856832, 0.22510381, 0.57838847, 0.19514078, 0.12633871, 0.61386397, 0.16392846, 0.26312341, 0.78464014, 0.38205329],
         [0.3771132 , 0.42317827, 0.88295305, 0.44258504, 0.7210982 , 0.71181544, 0.62802295, 0.73161301, 0.64498065, 0.24541482],
         [0.23418782, 0.03861684, 0.4098603 , 0.62496842, 0.66906535, 0.60161075, 0.76008686, 0.24457919, 0.65445907, 0.7220447]])

def normalize(x):
    return (x-x.std())/x.mean()

for j in range(X.shape[1]):
    X[:, j] = normalize(X[:, j])
#Y = np.matrix([1,-1,1]).T
Y = np.matrix([[1,0],[0,1],[1,0]])
threshold = 0.5

n, d = X.shape
n, c = Y.shape
W = np.matrix(np.ones((d-1, c)))

def Loss(W, X, Y):
    W = np.matrix(W).reshape((X.shape[1], Y.shape[1]))
    mat = np.dot(X, W) - Y
    return np.linalg.norm(mat, ord='fro')

def Regularized_term(W):
    W = np.matrix(W).reshape((X.shape[1], Y.shape[1]))
    arr = np.linalg.norm(W, ord=2, axis=1)
    return np.linalg.norm(arr, ord=1, axis=0)

def J(W, X, Y, threshold):
    res = Loss(W, X, Y)
    res += threshold*Regularized_term(W)
    return res

def F_J(w, W, X, Y, threshold):
    W=np.vstack((W, w))
    return J(W, X, Y, threshold)
def F_Loss(w, W, X, Y):
    W=np.vstack((W, w))
    return Loss(W, X, Y)

r=10
x, y=np.mgrid[-r:r:50j, -r:r:50j]
z_J = np.ones_like(x)
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        z_J[i, j] = F_J([x[i, j], y[i, j]], W, X, Y, threshold)

z_l21 = np.sqrt(x**2+y**2)

z_Loss = np.ones_like(x)
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        z_Loss[i, j] = F_Loss([x[i, j], y[i, j]], W, X, Y)

ax = plt.subplot(111,projection='3d')  
# ax.plot_surface(x,y,z_J,rstride=2,cstride=1,cmap=plt.cm.coolwarm,alpha=0.8) 
# ax.plot_surface(x,y,z_l21,rstride=2,cstride=1,cmap=plt.cm.coolwarm,alpha=0.8) 
ax.plot_surface(x,y,z_Loss,rstride=2,cstride=1,cmap=plt.cm.coolwarm,alpha=0.8) 

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
