import numpy as np# -*- coding: utf-8 -*-
## Q3 MSE

#def calculate_MSE_weights1(x,y):
#    x_ = x.mean(axis=0)
#    y_ = y.mean()
#    xy__ = [(x[:,0]*y).mean(),(x[:,1]*y).mean()]
#    
#    w = (xy__ - x_*y_)/((x**2).mean(axis=0) - x_**2)
#    b = y_ - np.matmul(w.T, x_) 
#    
#    y_pred = []
#    e = []
#    for i in range(4):
#        y_pred += [np.matmul(w.T,x[i]) + b]
#        e += [abs(y_pred[-1] - y[i])]
#    print(sum(e))


def calculate_MSE_weights2(xa1,x,y):
    # Convenient to use regular x for evaluating result
    R=np.matmul(np.transpose(xa1),xa1)
    Rinv=np.linalg.inv(R)
    r=np.matmul(y,xa1)
    w=np.dot(Rinv,r)
    b=w[-1] 
    w=w[:-1] # remove arbitrary ones
    y_pred = []
    e = []
    print(w)
    print(b)

    for i in range(4):
        y_pred += [np.matmul(w.T,x[i]) + b]
        e += [abs(y_pred[-1] - y[i])]
    print(sum(e))

## Recalculating inputs
x = np.array([[0,0],[0.1,1],[1,0.2],[1,1]])
xa1 = np.array([[0,0,1],[0.1,1,1],[1,0.2,1],[1,1,1]]) # Add one row of ones

y1 = np.array([0,0.41,0.18,0.5])
y2 = np.array([-0.416,0.3610,0.1222,0.473])

#calculate_MSE_weights1(x,y)
calculate_MSE_weights2(xa1,x,y1)
calculate_MSE_weights2(xa1,x,y2)


x_xor = np.array([[0,0],[0,1],[1,0],[1,1]])
x_xora1 = np.array([[0,0,1],[0,1,1],[1,0,1],[1,1,1]]) # add row of ones
y_xor = np.array([0,1,1,0])

calculate_MSE_weights2(x_xora1,x_xor,y_xor)

    
    
    
    
    
    