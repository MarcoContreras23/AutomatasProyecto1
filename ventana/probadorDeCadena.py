"""
Autores: Marco Contreras, Camilo Gomez
Version: 5.3
"""

class probadorDeCadena():
    def __init__(self,alf,estados,trans,inicial,final):
        self.alfabeto = alf
        self.estados = estados
        self.transiciones = trans
        self.inicial = inicial
        self.final = final
        self.Cadena = ""
        self.estadoCadena = False

    def comprobarCadena(self,Cadena):
        print("---------------------------------------------------")
        self.Cadena = Cadena
        self.copiaCadena = self.Cadena

        for est in self.inicial:
            self.Cadena = self.copiaCadena
            self.__comprobarCadena(est)
        if(self.estadoCadena == True):
            print("Valido")
            return True
        elif(self.estadoCadena == False):
            print("No valida")

    def __comprobarCadena(self,estado):
            print("Cadena: "+self.Cadena)
            print(estado)
            if self.Cadena:
                print("hay algo")
            else:
                print("no hay nada en la cadena")
                if(estado in self.final):
                    print("Valido recursivo")
                    self.estadoCadena = True
                    return
            transicionesValidas = self.buscasTransicionesValidasConEstados(estado)
            print("transvalidas: "+str(transicionesValidas))
            for trans in transicionesValidas:
                if(trans[2] == "λ"):
                    self.__comprobarCadena(trans[1])
                elif(self.Cadena):
                    if(self.verificarChardeCadena(trans)):
                        self.__comprobarCadena(trans[1])
                        self.backtracking()
                    else:
                        return

    def backtracking(self):
        print("Aqui iria el backtracking  copia"+self.copiaCadena+"  original  "+self.Cadena)
        cadSelf = list(self.Cadena)
        cadCopia = list(self.copiaCadena)
        cadAux = cadCopia[(len(cadCopia)-len(cadSelf)-1):]
        self.Cadena = ''.join(cadAux)

    def buscasTransicionesValidasConEstados(self,estado):
        transvalidos = []
        for tupla in self.transiciones:
            if(estado == tupla[0]):
                transvalidos.append(tupla)
        return transvalidos

    def verificarChardeCadena(self,tupla):
        if(tupla[2] == "λ"):
            return False
        else:
            charTupla = tupla[2]
            listCadena = list(self.Cadena)
            charCadena = listCadena.pop(0)
            if(charCadena == charTupla):
                self.Cadena = ''.join(listCadena)
                print("verificar: "+str(self.Cadena))
                return True
            else:
                return False

    def buscarTransicionesValidas(self,trans):
        transvalidas = []
        for tupla in self.transiciones:
            if(trans[1] == tupla[0]):
                transvalidas.append(tupla)
        return transvalidas

    def buscarInicial(self):
        tuplasinicialesaux = []
        for tupla in self.transiciones:
            if(tupla[0] in self.inicial):
                tuplasinicialesaux.append(tupla)
        return tuplasinicialesaux