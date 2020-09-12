# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 22:31:09 2020

@author: 56977
"""

from scipy.integrate import odeint
from leer_eof import leer_eof
import numpy as np
from sys import argv
from datetime import datetime, timedelta

nombre_eof = argv[1]

sat_t, sat_x, sat_y, sat_z, sat_vx, sat_vy, sat_vz = leer_eof(nombre_eof)

eof_salida = nombre_eof.replace(".EOF",".PRED")

Km = 1000.
omega = -7.2921150e-5
Km3 = (1000.)**3
Km5 = (1000.)**5
Km6 = (1000.)**6
mu = 398600441550000.000000
J2 = 1.75553e10*Km5
J3 = -2.61913e11*Km6


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
    
    
    zp[3:6] = R.T@(Fg+FJ2+FJ3-(2*Rp@xp+Rpp@x))
        
    return zp

t = sat_t

z0 = np.array([sat_x[0],sat_y[0],sat_z[0],sat_vx[0],sat_vy[0],sat_vz[0],])

sol = odeint(zpunto, z0, t)

x = sol[:,0]
y = sol[:,1]
z = sol[:,2]

vx = sol[:,3]
vy = sol[:,4]
vz = sol[:,5]

with open(eof_salida,"w") as fout:
    Nt = len(t)
    fout.write("<?xml version=\"1.0\"?>\n")
    fout.write("<Earth_Explorer_File>\n")
    fout.write("  <Earth_Explorer_Header>\n")
    fout.write("    <Fixed_Header>\n")
    fout.write("      <File_Name>S1B_OPER_AUX_POEORB_OPOD_20200828T111242_V20200807T225942_20200809T005942</File_Name>\n")
    fout.write("      <File_Description>Precise Orbit Ephemerides (POE) Orbit File</File_Description>\n")
    fout.write("      <Notes></Notes>\n")
    fout.write("      <Mission>Sentinel-1B</Mission>\n")
    fout.write("      <File_Class>OPER</File_Class>\n")
    fout.write("      <File_Type>AUX_POEORB</File_Type>\n")
    fout.write("      <Validity_Period>\n")
    fout.write("        <Validity_Start>UTC=2020-08-07T22:59:42</Validity_Start>\n")
    fout.write("        <Validity_Stop>UTC=2020-08-09T00:59:42</Validity_Stop>\n")
    fout.write("      </Validity_Period>\n")
    fout.write("      <File_Version>0001</File_Version>\n")
    fout.write("      <Source>\n")
    fout.write("        <System>OPOD</System>\n")
    fout.write("        <Creator>OPOD</Creator>\n")
    fout.write("        <Creator_Version>0.0</Creator_Version>\n")
    fout.write("        <Creation_Date>UTC=2020-08-28T11:12:42</Creation_Date>\n")
    fout.write("      </Source>\n")
    fout.write("    </Fixed_Header>\n")
    fout.write("    <Variable_Header>\n")
    fout.write("      <Ref_Frame>EARTH_FIXED</Ref_Frame>\n")
    fout.write("      <Time_Reference>UTC</Time_Reference>\n")
    fout.write("    </Variable_Header>\n")
    fout.write("  </Earth_Explorer_Header>\n")
    fout.write("<Data_Block type=\"xml\">\n  <List_of_OSVs count=\"9361\">\n")
    for i in range(Nt):
        obj = datetime(2020,8,7,22,59,42,000000)
        fecha = (obj + timedelta(seconds=t[i])).strftime("%Y-%m-%dT%H:%M:%S.%f")
        fout.write(f"    <OSV>\n      <UTC>UTC={fecha}</UTC>\n      <Absolute_Orbit>+22823</Absolute_Orbit>\n      <X unit=\"m\">{x[i]}</X>\n      <Y unit=\"m\">{y[i]}</Y>\n      <Z unit=\"m\">{z[i]}</Z>\n      <VX unit=\"m/s\">{vx[i]}</VX>\n      <VY unit=\"m/s\">{vy[i]}</VY>\n      <VZ unit=\"m/s\">{vz[i]}</VZ>\n      <Quality>NOMINAL</Quality>\n    </OSV>\n")
    fout.write("  </List_of_OSVs>\n</Data_Block>\n</Earth_Explorer_File>")