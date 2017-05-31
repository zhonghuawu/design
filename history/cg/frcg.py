import numpy as np

def frcg(fun,gfun,x0):
    maxk = 5000
    rho = 0.6
    sigma = 0.4
    k = 0
    epsilon = 1e-5
    n = np.shape(x0)[0]
    itern = 0
    while k < maxk:
        gk = gfun(x0)
        itern += 1
        itern %= n
        if itern == 1:
            dk = -gk
        else:
            beta = 1.0*np.dot(gk,gk)/np.dot(g0,g0)
            dk = -gk + beta*d0
            gd = np.dot(gk,dk)
            if gd >= 0.0:
                dk = -gk
        if np.linalg.norm(gk) < epsilon:
            break
        m = 0
        mk = 0
        while m < 20:
            if fun(x0+rho**m*dk) < fun(x0) + sigma*rho**m*np.dot(gk,dk):
                mk = m
                break
            m += 1
        x0 += rho**mk*dk
        g0 = gk
        d0 = dk
        k += 1  

    return x0,fun(x0),k
