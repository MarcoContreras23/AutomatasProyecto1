"""
Autores: Marco Contreras, Camilo Gomez
Version: 1.5
"""

#Clase que obtiene la expresion regular
class AutomataaExpresionRegular():
    def __init__(self,alf,estados,trans,inicial,final):
        self.alfabeto = alf
        self.estados = estados
        self.transiciones = trans
        self.inicial = inicial
        self.final = final
        self.ecuaciones = []

    def prueba(self):
        print("ESTRUCTURA")
        print(self.alfabeto)
        print(self.estados)
        print(self.transiciones)
        print(self.inicial)
        print(self.final)
        print("------------")

    def prueba2(self):
        largo = len(self.transiciones)
        conc = [[]]
        conc1 = ""
        for i in range(largo):
            for j in range(len(self.estados)):
                print(self.transiciones[i][0])
                print(self.inicial)
                if(self.transiciones[i][0] == self.estados[j]):
                    conc.insert(j,conc[j].append(str(self.transiciones[i][2]) + str(self.transiciones[i][1])))
                    self.ecuaciones.insert(j,conc)
        print("ACA")
        print(self.ecuaciones)



