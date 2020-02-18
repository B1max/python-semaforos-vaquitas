import threading
import time
import random
from puentes import Puente
class Animal(threading.Thread):
  semaforoCruzar = threading.Semaphore()
  semaforoAntesP = threading.Semaphore()
  myPuentes = []
  final = False
  idDePUenteActual = 99
  posBase=0
  indexPuente = 0
  direccion = '>'
  velocidad = 0.1
  def __init__(self,semaCruzar,semAntesP,puentes,posInicial,direccion,vel):
    super().__init__()
    self.posicion = posInicial
    self.velocidad = random.uniform(0.1, 0.5)
    self.semaforoCruzar = semaCruzar
    self.myPuentes = puentes
    self.semaforoAntesP = semAntesP
    self.direccion = direccion
    self.velocidad = vel

  def avanzar(self):
    # time.sleep(self.velocidad)
    time.sleep(0.1)
    self.posicion += 1
  def retroceder(self):
    time.sleep(0.1)
    self.posicion -= 1
  def mover(self, inicio,fin):
    self.semaforoCruzar.acquire()
    try:
      self.posicion==inicio
      # for i in range(inicio,fin,1):
      while self.posicion<=fin:
        self.avanzar()
    finally:
      self.semaforoCruzar.release()

  def dibujar(self):
    print(' ' * self.posicion + "🐮 " + str(self.idDePUenteActual) +'base'+str(self.posBase)+'index'+str(self.indexPuente)+'posB'+str(self.posBase))
  def acercarAinicio(self,inicioPuente):
    self.semaforoAntesP.acquire()
    try:
      for i in range(inicioPuente):
        if self.posicion<inicioPuente:
          self.avanzar()
          self.final-=1
    finally:
      self.semaforoAntesP.release()
  def cruzarPuente(self,finPuente):
    while self.posicion < finPuente and not (self.posicion > self.medirMaximoEnPuente()):
      self.semaforoCruzar.acquire()
      try:
          self.avanzar()
      finally:
        self.semaforoCruzar.release()

  def acercarAinicioInverso(self,inicioPuente):
    self.semaforoAntesP.acquire()
    try:
      for i in range(inicioPuente):
        if self.posicion>inicioPuente:
          self.retroceder()
          self.final-=1
    finally:
      self.semaforoAntesP.release()
  def cruzarPuenteInverso(self,iniPuente):
    while self.posicion > iniPuente:
      self.semaforoCruzar.acquire()
      try:
        self.retroceder()
      finally:
        self.semaforoCruzar.release()
  def medirMaximoEnPuente(self):
    max = 0
    for puente in self.myPuentes:
      max+=puente.getLargo()+puente.getInicio()
    return max
  def run(self):
    while(True):
      try:
        self.posBase = 0
        for puenteActual in self.myPuentes:
          if self.posicion < self.medirMaximoEnPuente():
            # self.idDePUenteActual = self.myPuentes[self.indexPuente].getId()
            self.acercarAinicio(self.posBase+puenteActual.getInicio())
            self.cruzarPuente(self.posBase+puenteActual.getInicio()+puenteActual.getLargo())
            self.posBase+=puenteActual.getInicio()+puenteActual.getLargo()
            # self.indexPuente+=1
            self.indexPuente=puenteActual.getId()

        for puenteActual in self.myPuentes.reverse():
          if self.posicion > 0:
            self.cruzarPuenteInverso(self.posBase-puenteActual.getLargo())
            self.acercarAinicioInverso(self.posBase-puenteActual.getLargo()-puenteActual.getInicio())
            self.posBase-=puenteActual.getInicio()+puenteActual.getLargo()
            self.indexPuente=puenteActual.getId()
      except:
        self.final = True