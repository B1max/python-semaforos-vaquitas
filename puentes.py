class Puente():
    id = 0
    largo = 0
    posInicio = 0
    def __init__(self,idE, inicio, largoE):
        self.id = idE
        self.posInicio = inicio
        self.largo = largoE
    def getInicio(self):
        return self.posInicio
    def getLargo(self):
        return self.largo
    def getId(self):
        return self.id