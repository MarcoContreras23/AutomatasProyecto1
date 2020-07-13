
"""
Autores: Marco Contreras, Camilo Gomez
Version: 6.3
"""


class Minimizador():
    def __init__(self,alf,estados,trans,inicial,final):
        self.alfabeto = alf
        self.estados = estados
        self.transiciones = trans
        self.inicial = inicial
        self.final = final
        self.igual = False
        self.transicionesResultante = []
        self.estadosResultante = []
        self.inicialResultante = []
        self.finalResultante = []
        self.pasos = []


    #Busca las transiciones que tiene cada estado y las adiciona a una lista
    def getTransiciones(self,estado,letra):
        transiciones = []
        for tupla in self.transiciones:
            if(tupla[0]==estado and tupla[2]==letra):
                transiciones.append(tupla[1])
        return transiciones

    def Minimizar(self):
        if('λ' in self.alfabeto):
            self.alfabeto.remove('λ')
        self.__minimizar()
        return [self.estadosResultante,
                self.inicialResultante,
                self.finalResultante,
                self.transicionesResultante,
                self.alfabeto,
                self.igual,
                self.pasos]

    def __minimizar(self):
        estados = list(self.estados)
        numEstados = len(self.estados)
        noComprobado = dict()
        cont = 1
        distinguido = []
        equivalente = dict(zip(range(len(estados)), [{est} for est in estados]))
        pos = dict(zip(estados, range(len(estados))))
        for i in range(numEstados - 1):
            for j in range(i + 1, numEstados):
                if not ([estados[i], estados[j]] in distinguido or [estados[j], estados[i]] in distinguido):
                    eq = 1
                    anexar = []
                    for char in self.alfabeto:
                        est1 = self.getTransiciones(estados[i], char)
                        est2 = self.getTransiciones(estados[j], char)
                        if len(est1) != len(est2):
                            eq = 0
                            break
                        if len(est1) > 1:
                            raise BaseException("afd con transiciones multiples")
                        elif len(est1) == 0:
                            continue
                        est1 = est1.pop()
                        est2 = est2.pop()
                        if est1 != est2:
                            if [est1, est2] in distinguido or [est2, est1] in distinguido:
                                self.pasos.append("Los estados "+str([est1, est2])+" son DISTINGUIBLES con los estados "+str(distinguido))
                                print("")
                                eq = 0
                                break
                            else:
                                self.pasos.append("Los estados "+str([est1, est2])+" son NO DISTINGUIBLES con los estados "+str(distinguido))
                                print("")

                                anexar.append([est1, est2, char])
                                eq = -1
                    if eq == 0:
                        distinguido.append([estados[i], estados[j]])
                    elif eq == -1:
                        est = [estados[i], estados[j]]
                        est.extend(anexar)
                        noComprobado[cont] = est
                        cont += 1
                    else:
                        p1 = pos[estados[i]]
                        p2 = pos[estados[j]]
                        if p1 != p2:
                            estad = equivalente.pop(p2)
                            for est in estad:
                                pos[est] = p1
                            equivalente[p1] = equivalente[p1].union(estad)
        encontrado = True
        while encontrado and len(noComprobado) > 0:
            self.pasos.append("SE COMPRUEBAN LOS VALORES NO COMPROBADOS PREVIAMENTE...")
            encontrado = False
            for par in noComprobado.items():
                for transi in par[2:]:
                    if [transi[0], transi[1]] in distinguido or [transi[1], transi[0]] in distinguido:
                        print("Los estados " + str([est1, est2]) + " son DISTINGUIBLES con los estados " + str(distinguido))
                        noComprobado.pop(p)
                        distinguido.append([par[0], par[1]])
                        encontrado = True
                        break
        for par in noComprobado.values():
            p1 = pos[par[0]]
            p2 = pos[par[1]]
            if p1 != p2:
                estad = equivalente.pop(p2)
                for est in estad:
                    pos[est] = p1
                equivalente[p1] = equivalente[p1].union(estad)
        if len(equivalente) == len(estados):
            self.igual = True
            print("Queda igual")
        else:

            for clave, valor in equivalente.items():
                self.pasos.append("El estado H%s es equivalente a los estados %s" % (clave, valor))

            self.nueva_Construcciondesde_estadosEquivalentes(equivalente,pos)

    def nueva_Construcciondesde_estadosEquivalentes(self,equivalente,pos):
        cont = 0
        self.sacarEstados(equivalente)
        for key in pos.keys():
            tuplas = self.sacarTupla(key,pos[key],pos)
            for tupla1 in tuplas:
                if(tupla1 not in self.transicionesResultante):
                    self.transicionesResultante.append(tupla1)
        self.pasos.append("Las nuevas transiciones generadas son:" + str(self.transicionesResultante))
        self.sacarIniciales(equivalente)
        self.sacarFinales(equivalente)

    def sacarIniciales(self,equivalente):
        for key in equivalente.keys():
            for valor in equivalente[key]:
                if (valor in self.inicial):
                    self.inicialResultante.append("H"+str(key))
                    break
        self.pasos.append("Los nuevos estados inicales son:" + str(self.inicialResultante))

    def sacarFinales(self,equivalente):
        for key in equivalente.keys():
            valorverdad = True
            for valor in equivalente[key]:
                if (valor not in self.final):
                    valorverdad = False
            if(valorverdad):
                self.finalResultante.append("H" + str(key))
        self.pasos.append("Los nuevos estados finales son:" + str(self.finalResultante))

    def sacarTupla(self,est,estRes,pos):
        tuplas = []
        for tupla in self.transiciones:
            if(tupla[0]==est):
                if(pos[tupla[1]] != None):
                    tupla = ("H"+str(estRes),"H"+str(pos[tupla[1]]),tupla[2])
                    tuplas.append(tupla)
        return tuplas
    def sacarEstados(self,equivalente):
        estados = []
        for key in equivalente.keys():
            estadoActual = "H"+str(key)
            estados.append(estadoActual)
        self.estadosResultante = estados;
        self.pasos.append("Los nuevos estados son: "+str(self.estadosResultante))