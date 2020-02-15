import os
import random
import time
import threading

inicioPuente = 10
largoPuente = 20
semaforo = threading.Semaphore(14)
semCruzar = threading.Semaphore(2)
class Puente():
  inicio = 0
  largo = 0
  def __init__(self,inicio,largo):
    self.inicio = inicio
    self.largo = largo
  def dibujar(self):
    print(' ' * self.inicio + '=' * self.largo)
class Vaca(threading.Thread):
  def __init__(self):
    super().__init__()
    self.posicion = 0
    self.velocidad = random.uniform(0.1, 0.5)
    # self.velocidad = 0.0001
  def avanzar(self):
    time.sleep(self.velocidad)
    self.posicion += 1

  def dibujar(self):
    print(' ' * self.posicion + "🐮")

  def run(self):
    while(True):
      if self.posicion < inicioPuente:
        semaforo.acquire()
        try:
          self.avanzar()
        finally:
          semaforo.release()
      else:
        while self.posicion < inicioPuente+largoPuente:     
          semCruzar.acquire()
          try:
            self.avanzar()
          finally:
            semCruzar.release()
vacas = []
for i in range(7):
  v = Vaca()
  vacas.append(v)
  v.start()

def cls():
  os.system('cls' if os.name=='nt' else 'clear')

def dibujarPuente():
  print(' ' * inicioPuente + '=' * largoPuente + ' ' * inicioPuente + '=' * largoPuente)

puente1 = Puente(11,24)
while(True):
  cls()
  print('Apretá Ctrl + C varias veces para salir...')
  print()
  puente1.dibujar()
  for v in vacas:
    v.dibujar()
  puente1.dibujar()
  time.sleep(0.2)
