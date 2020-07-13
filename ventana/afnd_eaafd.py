

import threading
import time

"""
Autores: Marco Contreras, Camilo Gomez
Version: 2.7
"""

class AFND_EaAFD():
    
    def __init__(self,alf,estados,trans,inicial,final,ventana):
        self.alfabeto = alf
        self.estados = estados
        self.transiciones = trans
        self.inicial = inicial
        self.final = final
        self.ventana = ventana
        self.contador = 0
        self.colaestados = []
        self.stringIRa = []

        #Aqui van las listas resultantes
        self.estadosResultante = []
        self.transicionesResultante = []
        self.inicialResultante = []
        self.finalResultante = []

        #Aqui van las listas con letras
        self.estadosResultanteaux = []
        self.transicionesResultanteaux = []
        self.inicialResultanteaux = []
        self.finalResultanteaux = []

    def convertirAFND_EaAFD(self):
        self.__convertirAFND_EaAFD()
        return [self.estadosResultanteaux,
                self.inicialResultanteaux,
                self.finalResultanteaux,
                self.transicionesResultanteaux,
                self.alfabeto,
                self.stringIRa]

    #Evalua el estado inicial y el estado resultante que tienen transicion lambda
    def __convertirAFND_EaAFD(self):
        estadoinicialresultante = self.CE(self.inicial)
        print("Paso a Paso")
        self.stringIRa.append("CE{"+str(self.inicial)+"}:"+str(estadoinicialresultante))
        if estadoinicialresultante:
            self.colaestados.append(estadoinicialresultante)
            self.estadosResultante.append(estadoinicialresultante)
        else:
            print("esta vacio")
            return
        while self.colaestados:
            self.Ira(self.colaestados.pop(0))
            self.contador += 1

        self.sacarEstadosInicialesyFinales()
        self.convertirestadosaletras()

    #Recorre el alfabeto
    def Ira(self,estados):
        for letra in self.alfabeto:
            if(letra != "λ"):
                mover = self.mover(estados,letra)
                CE = self.CE(mover)
                self.stringIRa.append("(Ir a " + "A" + str(self.contador) + "," + letra+"): "+
                      "CE(mover ("+"A" + str(self.contador)+","+letra+")): CE:{"+str(mover)+"}: "+str(CE))
                if len(CE)>0:
                    if(CE not in self.estadosResultante):
                        self.colaestados.append(CE)
                        self.estadosResultante.append(CE)
                    self.transicionesResultante.append((estados,CE,letra))

    def mover(self,estados,letra):
        resultadosmover = []
        for tupla in self.transiciones:
            for est in estados:
                if(tupla[2] == letra and tupla[0] == est):
                    resultadosmover.append(tupla[1])
        return resultadosmover


    def CE(self,estados):
        estadosCE = []
        for est in estados:
            estadosCE.append(est)
            self.__CE(est,estadosCE)
        return estadosCE

    def __CE(self,estado,estadosCE):
        for tupla in self.transiciones:
            if (estado == tupla[0]):
                if (tupla[2] == "λ" and tupla[1] not in estadosCE):
                    estadosCE.append(tupla[1])
                    self.__CE(tupla[1],estadosCE)

    def convertirestadosaletras(self):
        contador = 0
        for estado in self.estadosResultante:
            self.estadosResultanteaux.append("A"+str(contador))
            contador += 1
        for tupla in self.transicionesResultante:
            self.transicionesResultanteaux.append(("A"+str(self.estadosResultante.index(tupla[0])),
                                                  "A"+str(self.estadosResultante.index(tupla[1])),
                                                  tupla[2]))
        for estado in self.inicialResultante:
            self.inicialResultanteaux.append("A"+str(self.estadosResultante.index(estado)))
        for estado in self.finalResultante:
            self.finalResultanteaux.append("A" + str(self.estadosResultante.index(estado)))


    def sacarEstadosInicialesyFinales(self):
        for estado in self.estadosResultante:
            for final in self.final:
                if(final in estado):
                    if(estado not in self.finalResultante):
                        self.finalResultante.append(estado)
            for inicial in self.inicial:
                if (inicial in estado):
                    if (estado not in self.inicialResultante):
                        self.inicialResultante.append(estado)


