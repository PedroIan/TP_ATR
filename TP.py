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
qin = 0
qout = 0
h = 0
href = 0
R0 = 2.5
R1 = 5
H = 10


class process_thread(thr):
    def __init__(self):

        pass

    def run(self):
        sema.acquire()
        derivada = lambda h, t: (qin - uni(0.5, 1)*h**(1/2))/(pi*(R0 + ((R1 - R0)/H)*h)**2)
        timestamp = np.linspace(0,10, )
        sema.release()
        time.sleep(0.05)
        pass

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
