# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 14:30:48 2020

@author: 56977
"""

from scipy.integrate import odeint
import numpy as np
import matplotlib.pylab as plt
import sympy as sp

#definicion de parametros
m = 1
f = 1
epsilon = 0.2
w = 2*np.pi*f
ka = m*w**2
c = 2*epsilon*w*m


#ecuacion para determinar alfa, beta,C1 y C2 de la solucion de la EDO
x=sp.Function('x')
t=sp.symbols('t')

eq=sp.Eq(x(t).diff(t,2)+c*x(t).diff(t)+ka*x(t),0)

sol=sp.dsolve(eq,x(t)).rhs # x(t)

sold=sp.diff(sol,t) # x'(t)

x0=1
#to evaluate initial conditions - x(0)
cnd0=sp.Eq(sol.subs(t,0),x0)

xd0=1
#to evaluate initial conditions - derivative x'(0)
cnd1=sp.Eq(sold.subs(t,0),xd0)

c1c2 = list(sp.linsolve([cnd0,cnd1],sp.var('C1,C2')))

alpha = -1.25663706143592
beta = 6.15623918477695
C1 = 1
C2 = 0.366560978822281

def harmonic(z,t):
    zp = np.zeros(2)
    zp[0] = z[1]
    zp[1] = -(ka/m)*z[0] - (c/m)*z[1]
    
    return zp

def eulerint(harmonic,z0,t,Nsub=1):
    Nt = len(t)
    Ndim = len(z0)
    
    z = np.zeros((Nt,Ndim))
    z[0,:]=z0
    
    #z(i+1)=zp:i*dt+z_i
    for i in range(1,Nt):
        t_anterior = t[i-1]
        dt = (t[i]-t[i-1])/Nsub
        z_temp = z[i-1,:].copy() 
        for k in range(Nsub):
            z_temp+= dt*harmonic(z_temp,t_anterior+k*dt)
        z[i,:]=z_temp
          
    return z

z0 = np.array([1,1])
t = np.linspace(0, 4., 100)

z_odeint = odeint(harmonic,z0,t)
ode = z_odeint[:,0]

z_real = np.exp(alpha*t)*(np.cos(beta*t)*C1+np.sin(beta*t)*C2)

z_euler1 = eulerint(harmonic,z0,t,Nsub=1)
euler1 = z_euler1[:,0]

z_euler10 = eulerint(harmonic,z0,t,Nsub=10)
euler10 = z_euler10[:,0]

z_euler100 = eulerint(harmonic,z0,t,Nsub=100)
euler100 = z_euler100[:,0]

plt.plot(t,z_real,label="real",linewidth=2,color="k")
plt.plot(t,ode,label="odeint",color="b",linewidth=1)
plt.plot(t,euler1,"g--",label="eulerint (Nsub=1)")
plt.plot(t,euler10,"r--",label="eulerint (Nsub=10)")
plt.plot(t,euler100,"--",label="eulerint (Nsub=100)",color="orange")

plt.grid()
plt.legend()
plt.show()