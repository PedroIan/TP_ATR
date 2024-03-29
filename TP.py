import os
import random
from random import uniform as uni
import socket
import threading
from threading import Semaphore as sem
from threading import Lock as lock
from threading import Thread as thr
import numpy as np
from numpy import pi as pi
import time
import matplotlib.pyplot as plt
import sys
try:
    from scipy.integrate import odeint as EDO
except:
    os.system('python -m pip install scipy')



mut = lock()
maxIn = 10**(1/2)
qin = maxIn
qout = 0
h = []
h.append(0)
href = 5
R0 = 2.5
R1 = 5
H = 10


class process_thread(thr):
    def __init__(self, clientAddress = 0, clientsocket = 0):
        self.endCli = clientAddress
        self.sockCli = clientsocket
        thr.__init__(self)

    def run(self):
        while True:
            global mut, maxIn, qin, qout, h, href, R0, R1, H
            mut.acquire()
            qout = uni(0.5, 1)*(h[-1]**(1/2))
            #print("qout - ", qout)
            h.append(self.RungeKuttaSimples())
            mut.release()
            time.sleep(0.05)
            #print("entrou")
        self._stop()

    def volume(self, altura = 0):
        if altura <= 0:
            return 0
        else:
            r1 = 50/altura
            return pi*(R0**2 + R0*r1 + r1**2)*altura/3

    def volumeC(self, altura = 0):
        if altura < 0:
            return 0
        else:
            return pi*(R0**2)*altura

    def RungeKuttaSimples(self):
        try:
            #print(qin, qout, self.volumeC(h[-1]))
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
    def __init__(self, clientAddress = 0, clientsocket = 0):
        self.process = process_thread()
        self.endCli = clientAddress
        self.sockCli = clientsocket
        thr.__init__(self)
        pass

    def run(self):
        while True:
            global mut, maxIn, qin, qout, h, href, R0, R1, H
            mut.acquire()
            nexth = self.process.RungeKuttaSimples()
            if href < H:
                nextIn = self.process.volumeC(href) - self.process.volumeC(h[-1]) + qout
                #print("h atual - ", h[-1])
                if nextIn > maxIn:
                    qin = maxIn
                elif nextIn < 0:
                    qin = 0
                else:
                    qin = nextIn
                #print("qin atual -", qin)
            else:
                qin = self.process.volumeC(H) - self.process.volumeC(h[-1]) + qout
            try:
                self.sockCli.send(byte(qin), byte(qout), byte(h[-1]))
            except:
                pass
            mut.release()
            time.sleep(0.1)
        self._stop()

class synoptic(thr):
    def __init__(self):
        thr.__init__(self)

    def run(self):
        while True:
            global qin, qout, h, mut
            while True:
                sys.stdout.write("%-20s | %-20s | %-20s" % (str(h[-1]), str(qin), str(qout)))
                sys.stdout.flush()
                sys.stdout.write("\r") # return to start of line
                try:
                    mut.acquire()
                    href = input()
                    mut.release()
                except:
                    pass
                time.sleep(1)



LOCALHOST = "127.0.0.1"
PORT = 50000

#Conexão TCP/IP preparação para conexão cliente servidor (lado servidor)

print("Inicializando servidor de simulação....")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
#server.listen(1)
#clientsock, clientAddress = server.accept()

x = []
y = []
yerro = []
#pro = process_thread(clientsock, clientAddress)
pro = process_thread()
pro.start()
#plc = softPLC_thread(clientsock, clientAddress)
plc = softPLC_thread()
plc.start()

syn = synoptic()
syn.start()

time.sleep(5)
for i in range(len(h)-1):
    x.append(i)
    y.append(h[i])
    yerro.append(href - h[i])

plt.plot(x, y, label = 'Altura')
plt.xlabel('t(s)')
plt.ylabel('h(m)')
plt.title('Altura vs tempo')
plt.legend()
plt.draw()
plt.grid(b = True)
#plt.plot(x, yerro, label = 'Erro')
#plt.legend()
#plt.draw()
plt.show()
