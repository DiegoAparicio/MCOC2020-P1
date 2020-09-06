# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 20:37:16 2020

@author: 56977
"""

import matplotlib.pylab as plt
from scipy.integrate import odeint
#import datetime as dt
from leer_eof import leer_eof
import numpy as np

fname = "S1B_OPER_AUX_POEORB_OPOD_20200828T111242_V20200807T225942_20200809T005942.EOF"

sat_t, sat_x, sat_y, sat_z, sat_vx, sat_vy, sat_vz = leer_eof(fname)

correccion = 0

tmax = max(sat_t)

Km = 1000.
omega = -7.2921150e-5
Km3 = (1000.)**3
Km5 = (1000.)**5
Km6 = (1000.)**6
mu = 398600.440*Km3 #G*Mtierra
J2 = 1.75553e10*Km5
J3 = -2.61913e11*Km6
Radio = 6371.*Km
H0 = 700.*Km


def zpunto(z,t):
    c = np.cos(omega*t)
    s = np.sin(omega*t)
    
    R=np.array([[c,s,0],
       [-s,c,0],
       [0,0,1]])

    Rp=np.array([[-s,c,0],
        [-c,-s,0],
        [0,0,0]])*omega

    Rpp=np.array([[-c,-s,0],
         [s,-c,0],
         [0,0,0]])*omega**2
    
    x = z[0:3]
    xp = z[3:6]
    
    r = np.sqrt(np.dot(x,x))
    
    xstill = R@x
    rnorm = xstill/r
    Fg = -mu/r**2*rnorm
    
    z2 = xstill[2]**2
    rflat = xstill[0]**2 + xstill[1]**2
    FJ2 = J2*xstill/r**7
    FJ2[0] = FJ2[0]*(6*z2 -1.5*rflat)
    FJ2[1] = FJ2[1]*(6*z2 -1.5*rflat)
    FJ2[2] = FJ2[2]*(3*z2 -4.5*rflat)
    
    FJ3 = np.zeros(3)
    FJ3[0] = J3*xstill[0]*xstill[2]/r**9 * (10*z2 - 7.5*rflat)
    FJ3[1] = J3*xstill[1]*xstill[2]/r**9 * (10*z2 - 7.5*rflat)
    FJ3[2] = J3/r**9 * (4*z2 *(z2 - 3*rflat) +1.5*rflat**2) 
    
    
    zp = np.zeros(6)
    zp[0:3] = xp
    
    if correccion == 0:
        zp[3:6] = R.T@(Fg-(2*Rp@xp+Rpp@x))
    elif correccion == 1:
        zp[3:6] = R.T@(Fg+FJ2-(2*Rp@xp+Rpp@x))
    elif correccion == 2:
        zp[3:6] = R.T@(Fg+FJ2+FJ3-(2*Rp@xp+Rpp@x))
        
    return zp

t = sat_t
x0 = Radio + H0
vt = 6820.*3.6 #m/s

z0 = np.array([
    sat_x[0],
    sat_y[0],
    sat_z[0],
    sat_vx[0],
    sat_vy[0],
    sat_vz[0],
    ])

sol = odeint(zpunto, z0, t)

x = sol[:,0]
y = sol[:,1]
z = sol[:,2]


plt.figure()
plt.subplot(3,1,1)
plt.plot(sat_t/3600.,sat_x/1000)
plt.plot(t/3600.,x/1000)
plt.ylabel("$X$ (Km)")
plt.subplot(3,1,2)
plt.plot(sat_t/3600.,sat_y/1000)
plt.plot(t/3600.,y/1000)
plt.ylabel("$Y$ (Km)")
plt.subplot(3,1,3)
plt.plot(sat_t/3600.,sat_z/1000,label= "real")
plt.plot(t/3600.,z/1000,label="predicha")
plt.ylabel("$Z$ (Km)")
plt.suptitle("Posición")
plt.xlabel("Tiempo, $t$ (horas)")
plt.tight_layout(rect=[0,0.03,1,0.95])


plt.show()