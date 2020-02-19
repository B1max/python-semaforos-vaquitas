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
  test = 'no hice nada'
  def __init__(self,semaCruzar,semAntesP,puentes,posInicial,direccion,vel):
    super().__init__()
    self.posicion = posInicial
    self.velocidad = random.uniform(0.1, 0.5)
    self.semaforoCruzar = semaCruzar
    self.myPuentes = puentes
    self.semaforoAntesP = semAntesP
    self.velocidad = vel
    self.direccion = direccion
    self.inicirPos(direccion)
  def inicirPos(self, dir):
    if self.direccion == '<':
      self.posicion = self.medirMaximoEnPuente()
      self.test += 'set'
    else:
      self.direccion = dir

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
    print(' ' * self.posicion + "🐮 " + str(self.idDePUenteActual) +'base'+str(self.posBase)+'index'+str(self.indexPuente)+'posB'+str(self.posBase)+'test='+self.test)
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
      self.semaforoCruzar.acquire()
      try:
        while self.posicion < finPuente and not (self.posicion > self.medirMaximoEnPuente()):
          self.avanzar()
      finally:
        self.semaforoCruzar.release()

  def acercarAinicioInverso(self,inicioPuente):
    self.semaforoAntesP.acquire()
    try:
      # for i in range(inicioPuente):
      while self.posicion>inicioPuente:
        self.retroceder()
        # self.final-=1
    finally:
      self.semaforoAntesP.release()
  def cruzarPuenteInverso(self,iniPuente):
      self.semaforoCruzar.acquire()
      try:
        while self.posicion > iniPuente:
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
      # try:
      if self.direccion == '>':
        self.posBase = 0
        for puenteActual in self.myPuentes:
          if self.posicion < self.medirMaximoEnPuente() and self.direccion == '>':
            self.acercarAinicio(self.posBase+puenteActual.getInicio())
            self.cruzarPuente(self.posBase+puenteActual.getInicio()+puenteActual.getLargo())
            self.posBase+=puenteActual.getInicio()+puenteActual.getLargo()
            self.indexPuente=puenteActual.getId()

      if self.direccion == '<':
        self.test = 'inverso'
        self.myPuentes.reverse()
        for puenteActual2 in self.myPuentes:
          if self.posicion > 0:
            self.test = 'Soy inverso2'+self.direccion
            self.cruzarPuenteInverso(self.posBase-puenteActual2.getLargo())
            self.acercarAinicioInverso(self.posBase-puenteActual2.getLargo()-puenteActual2.getInicio())
            self.posBase-=puenteActual2.getInicio()+puenteActual2.getLargo()
            self.indexPuente=puenteActual2.getId()
      # except:
      #     self.final = True