# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:35:34 2020

@author: 56977
"""


import numpy as sp
from scipy.integrate import odeint


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

from datetime import datetime

ti = "2020-08-07T22:59:42.000000"
ti = ti.split("T")
ti = "{} {}".format(ti[0],ti[1])
ti = datetime.strptime(ti,"%Y-%m-%d %H:%M:%S.%f")
tf = "2020-08-09T00:59:42.000000"
tf = tf.split("T")
tf = "{} {}".format(tf[0],tf[1])
tf = datetime.strptime(tf,"%Y-%m-%d %H:%M:%S.%f")

deltaT = (tf-ti).total_seconds()

print("deltaT (Horas): ",deltaT/3600)

x_i=1370294.061606
y_i=-1298752.276157
z_i=-6825905.035159
vx_i=1583.004667
vy_i=-7203.515683
vz_i=1688.868285


x_f=2053236.062559
y_f=5747619.490888
z_f=-3589308.696382
vx_f=324.684219
vy_f=-4093.548228
vz_f=-6378.965330


t = sp.linspace(0,deltaT,9361) #tiempo 93600 segundos, 1 dia y dos horas


z0 = sp.array([x_i,y_i,z_i,vx_i,vy_i,vz_i]) #definimos posiciones y velocidades iniciales

sol = odeint(satelite,z0,t)

x = sol[:,:]

pos_final = sp.array([x_f,y_f,z_f,vx_f,vy_f,vz_f])-sol[-1]

print ("deriva de posicion en x: ",pos_final[0],"[m]")
print ("deriva de posicion en y: ",pos_final[1],"[m]")
print ("deriva de posicion en z: ",pos_final[2],"[m]")
print ("deriva de velocidad en x: ",pos_final[3],"[m/s]")
print ("deriva de velocidad en y: ",pos_final[4],"[m/s]")
print ("deriva de velocidad en z: ",pos_final[5],"[m/s]")




