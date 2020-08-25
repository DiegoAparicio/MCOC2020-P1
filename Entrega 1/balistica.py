# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 09:48:20 2020

@author: 56977
"""

import scipy as sp
from scipy.integrate import odeint

#parametros:

p = 1.225 #kg/m3
cd = 0.47
cm = 0.01
inch = 2.54*cm
D = 8.5*inch   
r = D/2
A = sp.pi*r**2

CD = 0.5*p*cd*A

g = 9.81 #m/s2

m = 15

Vs = [0,10.,20.]
#V = 20
#funcion a integrar:

for V in Vs: 
    def bala(z,t):
        zp = sp.zeros(4)
        zp[0] = z[2]
        zp[1] = z[3]
        v = z[2:4]
        v[0]= v[0]-V #velocidad menos viento
        vnorm = sp.sqrt(sp.dot(v,v))
        FD = -CD*sp.dot(v,v)*(v/vnorm)
        zp[2] = FD[0]/m
        zp[3] = FD[1]/m -g
        
        return zp
    
    #vector de tiempo
    
    t = sp.linspace(0,30,1001)
    
    #parte en el origen y tiene vx=vy=2 m/s
    vi = 100*1000/3600
    z0 = sp.array([0,0,vi,vi])
    
    sol = odeint(bala,z0,t)
    
    import matplotlib.pylab as plt
    
    x = sol[:,0]
    y = sol[:,1]
    
    plt.figure(1)
    plt.title("Trayectoria para distintos vientos")
    plt.grid()
    plt.axis([0,150,0,50])
    plt.plot(x,y,label =f"V = {V} m/s")
    plt.ylabel("Y (m)")
    plt.xlabel("X (m)")
plt.legend(loc="upper right")
plt.savefig("trayectoria.png")
plt.show()





