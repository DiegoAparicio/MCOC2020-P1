# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:24:54 2020

@author: 56977
"""
import scipy as sp
from scipy.integrate import odeint
import matplotlib.pylab as plt


#datos satelite

ms = 2300 #masa satelite en Kg
mt = 5.972e24 #masa de la tierra en Kg
r = 7071000 #distancia del centro de la tierra al satelite en m
g = 9.81 #gravedad m/s2
G = 6.67e-11 #Constante de gravitacion universal
W = 7.27e-5 #velocidad angular de la tierra rad/s




def satelite(z,t):
    #matrices de rotacion
    R=sp.array([[sp.cos(W*t),-sp.sin(W*t),0],
       [sp.sin(W*t),sp.cos(W*t),0],
       [0,0,1]])

    Rp=sp.array([[-sp.sin(W*t),-sp.cos(W*t),0],
        [sp.cos(W*t),-sp.sin(W*t),0],
        [0,0,0]])*W

    R2p=sp.array([[-sp.cos(W*t),sp.sin(W*t),0],
         [-sp.sin(W*t),-sp.cos(W*t),0],
         [0,0,0]])*W**2
    
    zp = sp.zeros(6)
    zp[0:3] = z[3:6]
    zp[3:6] = (-G*mt/r**3)*z[0:3]-R.T@(R2p@z[0:3]+2*Rp@z[3:6]) #ecuacion de estado
    return zp

t = sp.linspace(0,12700,1001) #tiempo 12700 segundos, suficiente para dar 2 orbitas completas.

vt = (G*mt/r)**(1/2)  #velocidad minima para mantener orbita 7505.55 m/s aprox.

z0 = sp.array([r,0,0,0,vt,0]) #definimos posicion inicial r en x y velocidad inicial vt en y.

sol = odeint(satelite,z0,t)

x = sol[:,0]
y = sol[:,1]
z = sol[:,2]

plt.figure(1) #grafico de orbita satelital
circle1 = plt.Circle((0, 0),6371000, color='#A6CAE0',alpha = 0.5,label ="Superficie terrestre")
circle2 = plt.Circle((0, 0),6451000, color='r',alpha = 0.5,fill=False,label ="Atmosfera")
fig, ax = plt.subplots()
plt.title("Trayectoria Satelital")
plt.xlim(-8500000,8000000)
plt.ylim(-8500000,8000000)
ax.add_artist(circle2)
ax.add_artist(circle1)
ley_tierra = ax.legend(handles=[circle1],loc="center")
ax.add_artist(ley_tierra)
ley_atm = ax.legend(handles=[circle2],loc="upper right")
ax.add_artist(ley_atm)
plt.plot(x,y,color="b",label ="Orbita satelite")
plt.ylabel("Y (m)")
plt.xlabel("X (m)")
plt.legend(loc="lower left")
plt.show()

plt.figure(2) #Grafico de historias de tiempo para dos orbitas
plt.title("Historias de tiempo")
plt.plot(t,x,label= "X(t)" )
plt.plot(t,y,label= "Y(t)" )
plt.plot(t,z,label= "Z(t)" )
plt.ylabel("Y (m)")
plt.xlabel("X (m)")
plt.legend()
plt.grid()
plt.show()



