import os
import random
from random import uniform as uni
import socket
import threading
from threading import Semaphore as sem
from threading import Thread as thr
import numpy as np
from numpy import pi as pi
import time
try:
    from scipy.integrate import odeint as EDO
except:
    os.system('python -m pip install scipy')

sema = sem()
maxIn = 10**(1/2)
qin = 7
qout = 0
h = []
h.append(0)
href = 0
R0 = 2.5
R1 = 5
H = 10


class process_thread(thr):
    def __init__(self):
        thr.__init__(self)

    def run(self):
        while True:
            sema.acquire()
            qout = uni(0.5, 1)*(h[-1]**(1/2))
            h.append(self.RungeKuttaSimples())
            sema.release()
            time.sleep(0.05)
            #print("entrou")
        self._stop()

    def volume(self, altura = 0):
        if altura == 0:
            return 0
        else:
            r1 = 25/altura
            return pi*(R0**2 + R0*r1 + r1**2)*altura/3

    def volumeC(self, altura = 0):
        if altura < 0:
            return 0
        else:
            return pi*(R0**2)*altura

    def RungeKuttaSimples(self):
        try:
            return (qin - qout + self.volumeC(h[-1]))/(pi*(R0**2))
        except:
            pass

    def RungeKutta(self, x, fx, n = 3, hs = 0.05):
        k1 = []
        k2 = []
        k3 = []
        k4 = []
        xk = []
        for i in range(n):
            k1.append(fx[i](x)*hs)
        for i in range(n):
            xk.append(x[i] + k1[i]*0.5)
        for i in range(n):
            k2.append(fx[i](xk)*hs)
        for i in range(n):
            xk[i] = x[i] + k2[i]*0.5
        for i in range(n):
            k3.append(fx[i](xk)*hs)
        for i in range(n):
            xk[i] = x[i] + k3[i]
        for i in range(n):
            k4.append(fx[i](xk)*hs)
        for i in range(n):
            x[i] = x[i] + (k1[i] + 2*(k2[i] + k3[i]) + k4[i])/6
        return x


class softPLC_thread(thr):
    def __init__(self):
        self.process = process_thread()
        thr.__init__(self)
        pass

    def run(self):
        while True:
            sema.acquire()
            nexth = self.process.RungeKuttaSimples()
            if href < H:
                nextIn = self.process.volumeC(href) - self.process.volumeC(h[-1]) + qout
                print(h[-1])
                if nextIn > maxIn:
                    qin = maxIn
                elif nextIn < 0:
                    qin = 0
                else:
                    qin = nextIn
                print(qin)
            else:
                qin = self.process.volumeC(H) - self.process.volumeC(h[-1]) + qout
            sema.release()
            time.sleep(0.1)
        self._stop()




href = int(input())
pro = process_thread()
pro.start()
plc = softPLC_thread()
plc.start()
time.sleep(5)
for i in range(len(h)):
    print(h[i], h[i] - h[i - 1])
