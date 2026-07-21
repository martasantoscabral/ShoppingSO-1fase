#!/usr/bin/env python3
# imports:

import os, time, sys
from multiprocessing import Queue
from threading import Thread

# Verificar argumento
if len(sys.argv) != 2:
    print("Uso: analisar_cliente.py <caminho_ficheiro_csv>")


# Thread 1: artigos caros (>1000€)
def thread1():
    #Consome a primeira linha (cabeçalho).
    fila1.get()
    #indice referente a coluna preco.
    coluna_preco=3
    coluna_produto = 2
    while (1):
        linha = fila1.get()
        if linha == None:
            break
        linha = linha.strip().split(",")
        if float(linha[coluna_preco])>1000.0:
            preco = linha[coluna_preco] 
            produto = linha[coluna_produto]
            print(f"[{caminho_ficheiro_csv.split("/")[-1].split('.')[0]}:T1] Compras Caras: " + produto + " -> " + preco + "€")
       
        time.sleep(0.01)


# Thread 2: total gasto
def thread2():
    #Consome a primeira linha (cabeçalho).
    fila2.get()
    total_gasto = 0
    while (1):
        linha = fila2.get()
        if linha == None:
           print(f"[{caminho_ficheiro_csv.split("/")[-1].split('.')[0]}:T2] Total gasto: {round(total_gasto,2)}€")
           break
        linha = linha.strip().split(",")
        preco = linha[3]
        total_gasto += float(preco)
        time.sleep(0.01)


# Thread 3: compras nos dias 29,30,31
def thread3():
    #Consome a primeira linha (cabeçalho).
    fila3.get()
    #indice referente a coluna data.
    coluna_data = 0
    coluna_produto = 2
    
    while (1):
        linha = fila3.get()
        if linha is None:
            break
            
        linha = linha.strip().split(",")
        data = linha[coluna_data].strip()
        produto = linha[coluna_produto].strip()

        #obter o dia da data
        dia = int(data.split("-")[2])
        
        #produtos dias especiais 
        if dia in (29, 30, 31):
            print(f"[{caminho_ficheiro_csv.split("/")[-1].split('.')[0]}:T3] Compra dia especial: {produto} -> {data}")
        time.sleep(0.01)

# -- Main thread --

# Análise iniciada.
caminho_ficheiro_csv = sys.argv[1]
ficheiro = caminho_ficheiro_csv.split("/")[-1].split('.')[0]
print(f"[{ficheiro}:main] Análise iniciada.")
# ....
#print(f"{caminho_ficheiro_csv=}")

#Criar as 3 filas (uma para cada thread)
fila1 = Queue(5)
fila2 = Queue(5)
fila3 = Queue(5)

#Criar uma fila de threads
lista_threads=[]

#Adicionar cada uma das threads na lista de threads
lista_threads.append(Thread(target=thread1))
lista_threads.append(Thread(target=thread2))
lista_threads.append(Thread(target=thread3))

#Inicializar cada uma das threads sequencialmente.
for thread in lista_threads:
 thread.start()

#Colocar cada uma das linhas do ficheiro em cada uma das filas.
with open(caminho_ficheiro_csv,"r") as ficheir:
 for linha in ficheir:
  fila1.put(linha)
  fila2.put(linha)
  fila3.put(linha)

#Colocar None no final para a thread saber quando deve parar de receber mensagens(quando não houver mais linhas de ficheiro na fila, thread recebe None e interrompe while).
fila1.put(None)
fila2.put(None)
fila3.put(None)

#Fazer join em cada uma das threads sequencialmente.
for thread in lista_threads:
 thread.join()


# Análise concluída.
print(f"[{ficheiro}:main] Análise concluida.")
