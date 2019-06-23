# -*- coding: utf-8 -*-
import random
import socket
import threading
import pickle
import base

sema = threading.Semaphore()

#Conexao CLIENTE-SERVIDOR

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



LOCALHOST = "127.0.0.1"
PORT = 50000

#Conexão TCP/IP preparação para conexão cliente servidor (lado servidor)

print("Inicializando servidor....")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Esperando por requisições.............")

#Variável auxiliar para receber clientes
aux_count_Clientes = 0
dealer = base.dealer()
jogador = base.player()
newThreads = []
mesa = []
while (aux_count_Clientes < 4):
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newThreads.append(ClientThread(clientAddress, clientsock, dealer, aux_count_Clientes))
    newThreads[aux_count_Clientes].start()
    aux_count_Clientes += 1

#Descobrir quem é o primeiro a jogar
aux = 0
playAtual = -1
rodada = 0
for i in newThreads:
    for k in i.player:
        if k.valor == 0:
            playAtual = aux
            break
    if playAtual != aux:
        aux += 1
    else:
        break

while True:
    typeAtual = 0 #1 singles, 2 dupla, 3 trinca, 4 sequencia, 5 flush, 6 fullhouse, 7 quadra
    typeJogada = 0 #1 singles, 2 dupla, 3 trinca, 4 sequencia, 5 flush, 6 fullhouse, 7 quadra
    highest = 0 #maior carta da jogada
    mesaTemp = []
    try:
        if newThreads[playAtual].jogadas[0].valor == dealer.mesa[0].valor:
            rodada = 0
            dealer.mesa = []
    except: pass
    if not dealer.mesa:
        newThreads[playAtual].sockCli.send(bytes("Sua vez de jogar, mesa vazia", "UTF-8"))
    else:
        newThreads[playAtual].sockCli.send(bytes("Sua vez de jogar", "UTF-8"))
        newThreads[playAtual].sockCli.send(pickle.dumps(dealer.mesa))
    try:
        mesaTemp = newThreads[playAtual].jogadas
        mesaTemp = jogador.orgNum(mesaTemp)
    except: pass
    try:
        typeJogada = mesaTemp[-1].valor
    except:
        typeJogada = 0

    try:
        highest = dealer.mesa[-1].valor
    except: pass
    while len(mesaTemp) != len(dealer.mesa) and rodada != 0 or highest > typeJogada:
        if not mesaTemp:
            break
        newThreads[playAtual].sockCli.send(bytes("Jogada invalida", "UTF-8"))
        try:
            mesaTemp = pickle.loads(newThreads[playAtual].sockCli.recv(2048))
        except:
            pass
    if mesaTemp:
        if dealer.checka(dealer.mesa, mesaTemp):
            dealer.mesa = mesaTemp
            newThreads[playAtual].jogadas = mesaTemp
            highest = dealer.mesa[-1].valor
        elif not dealer.mesa:
            dealer.mesa = mesaTemp
            newThreads[playAtual].jogadas = mesaTemp
            highest = dealer.mesa[-1].valor
        rodada += 1
    else:
        rodada += 0

    print(highest)

    for i in mesaTemp:
        for k in newThreads[playAtual].player:
            if i.numero == k.numero and i.nipe == k.nipe:
                newThreads[playAtual].player.remove(k)
    playAtual = (playAtual + 1)%4
    len1 = len(newThreads[playAtual].player)
    len2 = len(newThreads[(playAtual + 1)%4].player)
    len3 = len(newThreads[(playAtual + 2)%4].player)
    len4 = len(newThreads[(playAtual + 3)%4].player)
    if not len1 or not len2 or not len3 or not len4:
        newThreads[playAtual].sockCli.close()
        newThreads[(playAtual + 1)%4].sockCli.close()
        newThreads[(playAtual + 2)%4].sockCli.close()
        newThreads[(playAtual + 3)%4].sockCli.close()


    print("Dê o comando finalizador da rodada:")
    cS = input()
    while cS != 'exit':
        if cS == 'tam':
            print(len1, len2, len3, len4)
        elif cS == 'mesa':
            jogador.printJogadas(dealer.mesa)
        elif cS == 'atual':
            print(playAtual)
        else:
            print("Comando inválido")
        cS = input()
