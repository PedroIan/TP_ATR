import random
import socket
import threading
from threading import Semaphore as sem
from threading import Thread as thr
import pickle
import base

sema = sem()
qin = 0
qout = 0
h = 0
href = 0


class process_thread(thr):
    def __init__(self):

        pass
    def run(self):
        pass

class softPLC_thread(thr):
    def __init__(self):
        pass
    def run(self):
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
