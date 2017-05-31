# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 15:01:54 2016
@author: zhangweiguo
"""
import sympy,numpy
import math
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D as ax3
#import SD#这个文件里有最速下降法SD的方法，参见前面的博客
#共轭梯度法FR、PRP两种格式
def CG_FR(x0,N,E,f,f_d):
    X=x0;Y=[];Y_d=[];
    n = 1
    ee = f_d(x0)
    e=(ee[0]**2+ee[1]**2)**0.5
    d=-f_d(x0)
    Y.append(f(x0)[0,0]);Y_d.append(e)
    a=sympy.Symbol('a',real=True)
    print '第%2s次迭代：e=%f' % (n, e)
    while n<N and e>E:
        n=n+1
        g1=f_d(x0)
        f1=f(x0+a*f_d(x0))
        a0=sympy.solve(sympy.diff(f1[0,0],a,1))
        x0=x0-d*a0
        X=numpy.c_[X,x0];Y.append(f(x0)[0,0])
        ee = f_d(x0)
        e = math.pow(math.pow(ee[0,0],2)+math.pow(ee[1,0],2),0.5)
        Y_d.append(e)
        g2=f_d(x0)
        beta=(numpy.dot(g2.T,g2))/numpy.dot(g1.T,g1)
        d=-f_d(x0)+beta*d
        print '第%2s次迭代：e=%f'%(n,e)
    return X,Y,Y_d
def CG_PRP(x0,N,E,f,f_d):
    X=x0;Y=[];Y_d=[];
    n = 1
    ee = f_d(x0)
    e=(ee[0]**2+ee[1]**2)**0.5
    d=-f_d(x0)
    Y.append(f(x0)[0,0]);Y_d.append(e)
    a=sympy.Symbol('a',real=True)
    print '第%2s次迭代：e=%f' % (n, e)
    while n<N and e>E:
        n=n+1
        g1=f_d(x0)
        f1=f(x0+a*f_d(x0))
        a0=sympy.solve(sympy.diff(f1[0,0],a,1))
        x0=x0-d*a0
        X=numpy.c_[X,x0];Y.append(f(x0)[0,0])
        ee = f_d(x0)
        e = math.pow(math.pow(ee[0,0],2)+math.pow(ee[1,0],2),0.5)
        Y_d.append(e)
        g2=f_d(x0)
        beta=(numpy.dot(g2.T,g2-g1))/numpy.dot(g1.T,g1)
        d=-f_d(x0)+beta*d
        print '第%2s次迭代：e=%f'%(n,e)
    return X,Y,Y_d
if __name__=='__main__':
    '''
    G=numpy.array([[21.0,4.0],[4.0,15.0]])
    #G=numpy.array([[21.0,4.0],[4.0,1.0]])
    b=numpy.array([[2.0],[3.0]])
    c=10.0
    x0=numpy.array([[-10.0],[100.0]])
    '''
    
    m=4
    T=6*numpy.eye(m)
    T[0,1]=-1;T[m-1,m-2]=-1
    for i in xrange(1,m-1):
        T[i,i+1]=-1
        T[i,i-1]=-1
    W=numpy.zeros((m**2,m**2))
    W[0:m,0:m]=T
    W[m**2-m:m**2,m**2-m:m**2]=T
    W[0:m,m:2*m]=-numpy.eye(m)
    W[m**2-m:m**2,m**2-2*m:m**2-m]=-numpy.eye(m)
    for i in xrange(1,m-1):
        W[i*m:(i+1)*m,i*m:(i+1)*m]=T
        W[i*m:(i+1)*m,i*m+m:(i+1)*m+m]=-numpy.eye(m)
        W[i*m:(i+1)*m,i*m-m:(i+1)*m-m]=-numpy.eye(m)
    mm=m**2
    mmm=m**3
    G=numpy.zeros((mmm,mmm))
    G[0:mm,0:mm]=W;G[mmm-mm:mmm,mmm-mm:mmm]=W;
    G[0:mm,mm:2*mm]=-numpy.eye(mm)
    G[mmm-mm:mmm,mmm-2*mm:mmm-mm]=-numpy.eye(mm)
    for i in xrange(1,m-1):
        G[i*mm:(i+1)*mm,i*mm:(i+1)*mm]=W
        G[i*mm:(i+1)*mm,i*mm-mm:(i+1)*mm-mm]=-numpy.eye(mm)
        G[i*mm:(i+1)*mm,i*mm+mm:(i+1)*mm+mm]=-numpy.eye(mm)
    x_goal=numpy.ones((mmm,1))
    b=-numpy.dot(G,x_goal)
    c=0
    f = lambda x: 0.5 * (numpy.dot(numpy.dot(x.T, G), x)) + numpy.dot(b.T, x) + c
    f_d = lambda x: numpy.dot(G, x) + b
    x0=x_goal+numpy.random.rand(mmm,1)*100
    N=100
    E=10**(-6)
    print '共轭梯度PR'
    X1, Y1, Y_d1=CG_FR(x0,N,E,f,f_d)
    print '共轭梯度PBR'
    X2, Y2, Y_d2=CG_PRP(x0,N,E,f,f_d)
    figure1=pl.figure('trend')
    n1=len(Y1)
    n2=len(Y2)
    x1=numpy.arange(1,n1+1)
    x2=numpy.arange(1,n2+1)
    
    # X3, Y3, Y_d3=SD.SD(x0,N,E,f,f_d)
    # n3=len(Y3)
    # x3=range(1,n3+1)
    # pl.semilogy(x3,Y3,'g*',markersize=10,label='SD:'+str(n3))
    pl.semilogy(x1,Y1,'r*',markersize=10,label='CG-FR:'+str(n1))
    pl.semilogy(x2,Y2,'b*',markersize=10,label='CG-PRP:'+str(n2))
    # pl.legend()
    #图像显示了三种不同的方法各自迭代的次数与最优值变化情况，共轭梯度方法是明显优于最速下降法的
    pl.xlabel('n')
    pl.ylabel('f(x)')
    pl.show()