import os
import random
import time
import threading
from animales import Animal
from puentes import Puente

inicioPuente = 10
largoPuente = 20
vacasPorPuente = 2
totalVacas = 5
semVacasPorPuente = threading.Semaphore(vacasPorPuente)
semVacasAntesDelPuente = threading.Semaphore(totalVacas)
vacas = []
listaDePuentes = []

listaDePuentes.append(Puente(0,11,24))
listaDePuentes.append(Puente(1,11,24))
    
for i in range(totalVacas):
  # v = Vaca(semVacasPorPuente,semVacasAntesDelPuente,ListaDePuentes)
  # v = Vaca(semVacasPorPuente,semVacasAntesDelPuente,[Puente(0,11,24),Puente(0,11,24)])
  v = Animal(semVacasPorPuente,semVacasAntesDelPuente,listaDePuentes,0,'>',1)
  vacas.append(v)
  v.start()

def cls():
  os.system('cls' if os.name=='nt' else 'clear')

def dibujarPuente():
  dib =''
  for puente in listaDePuentes:
    dib+=(' ' * puente.getInicio() + 'm' * puente.getLargo())
  print(dib)

while(True):
  cls()
  print(f'Apretá Ctrl + C varias veces para salir...puentes ={len(listaDePuentes)}')
  print()
  dibujarPuente()
  for v in vacas:
    v.dibujar()
  dibujarPuente()
  time.sleep(0.2)