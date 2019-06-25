import os
import random
from random import uniform as uni
import socket
import threading
from threading import Semaphore as sem
from threading import Thread as thr
import numpy as np
from numpy import pi as pi
try:
    from scipy.integrate import odeint as EDO
except:
    os.system('python -m pip install scipy')

sema = sem()
maxIn = 7
qin = 0
qout = 0
h = 0
href = 0
R0 = 2.5
R1 = 5
H = 10


class process_thread(thr):
    def __init__(self):
        self.h = []
        self.h.append(h)
        thr.__init__(self)

    def run(self):
        sema.acquire()
        self.RungeKuttaSimples()
        sema.release()
        time.sleep(0.05)

    def RungeKuttaSimples(self):
        try:
            nextH = 2*self.h[-1] - self.h[-2] 
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
        pass

    def run(self):

        time.sleep(0.1)
        pass



class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, dealer = base.dealer(), jogadas = [], posi = 0):

        self.player = dealer.distribuicao()
        self.endCli = clientAddress
        self.jogadas = jogadas

        threading.Thread.__init__(self)
        self.sockCli = clientsocket
        self.data = 0

        print("Nova conexão, endereço do cliente: ",self.endCli)

    def run(self):
        print("Conexao com: ", self.endCli)

        #Real comunicação entre cliente e servidor
        while True:
            self.data = self.sockCli.recv(2048)
            if not self.data:
                break
            try:
                if self.data == b'get':
                    self.sockCli.send(pickle.dumps(self.player))
                elif self.data == b'bye':
                    break
            except: pass
            try:
                self.jogadas = pickle.loads(self.data)
            except: pass
        self.sockCli.close()
        print("Cliente com endereço ", self.endCli, " desconectado...")
        self._stop()
