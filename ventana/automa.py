import graphviz as gv
from subprocess import check_call
from tkinter import *
import Pila
import Minimizador
import time
import graficarManualmente
import threading
from VentanaInicial import ExpresionRegular
import PIL
import afnd_eaafd
from PIL import Image
import probadorDeCadena
import easygui as eg
import AutomataaExpresionRegular

"""
Autores: Marco Contreras, Camilo Gomez
Version: 8.2
"""

# Todos los parámetros son listas o tuplas
# donde:
#  * alfabeto:  es el alfabeto aceptado por el
#               autómata.
#  * estados:   es una lista de estados aceptados
#               por el autómata.
#  * inicio:    Son los estados de inicio del fsm.
#  * trans:     Es una tupla de funciones de transición
#               con tres elementos que son: (a,b,c) donde
#               (a,b) son los estados de partida y llegada;
#               mientras que c es la letra que acepta.
#  * final      Son los estados finales del autómata.

class GraficadoraAutomatas():
    def __init__(self,EP,alf):
        self.ventana = Tk()
        self.posfija = EP
        self.alfabeto = alf
        self.alfabeto = self.mayuscula(self.alfabeto)
        self.alfabeto.append("λ")
        self.estados = []
        self.terminal = []
        self.inicial = []
        self.trans = []

    def crear(self):
        self.ventana.title("Graficadora")
        self.ventana.geometry('1200x500')
        self.ventana.resizable(False, False)
        self.ventana.configure(background="white")



        #Dibujar Grafo
        """
        img = PhotoImage(file="C:\\Users\\marco\\OneDrive\\Documentos\\Automatas\\Automatasproyecto1\\ventana\\Digraph.gif")
        can = Canvas(self.ventana)
        can.pack(fill=BOTH)
        can.create_image(20, 20, image=img, anchor=NW)
        """

        #Crear barra de naveagcion
        barMenu = Menu(self.ventana)

        #CREAR MENU
        menuOpciones = Menu(barMenu,tearoff=0)

        #SUBMENUS
        menuOpciones.add_command(label="Expresión Regular",command=self.ingresarExpresionRegular)
        #menuOpciones.add_command(label="Graficar", command=self.ingresarGraficoManual)
        menuOpciones.add_command(label="AFND a AFD", command=self.converirAFND_EaAFD)
        menuOpciones.add_command(label="Minimizar", command=self.minimizar)
        #menuOpciones.add_command(label="AUT a ER", command=self.metodo)
        menuOpciones.add_command(label="Probar Cadena", command=self.probarCadena)

        #Agregar a la barra principal
        barMenu.add_cascade(label="Opciones",menu=menuOpciones)

        self.ventana.config(menu=barMenu)

    #Muestra el paso a paso de la conversion de AFND a FND
    def minimizar(self):
        print("MINIMIZAR")
        min = Minimizador.Minimizador(self.alfabeto,self.estados,self.trans,self.inicial,self.terminal)
        res = min.Minimizar()
        for paso in res[6]:
            eg.msgbox(msg=''+str(paso),
                      title='MINIMIZADOR',
                      ok_button='Siguiente paso',
                      image=None)

        if(res[5] == False):
            self.generarDigraphdesdeAUT(res[0], res[1], res[2], res[3], res[4])
        else:
            eg.msgbox(msg='El automata ya está minimizado',
                      title='AFND-EaAFD',
                      ok_button='Aceptar',
                      image=None)

    #Muestra el paso a paso de la conversion de AFND a FND
    def converirAFND_EaAFD(self):

        afnd = afnd_eaafd.AFND_EaAFD(self.alfabeto,self.estados,self.trans,self.inicial,self.terminal,self)
        res = afnd.convertirAFND_EaAFD()
        for paso in res[5]:
            eg.msgbox(msg=''+str(paso),
                      title='AFND-EaAFD',
                      ok_button='Siguiente paso',
                      image=None)
        self.generarDigraphdesdeAUT(res[0],res[1],res[2],res[3],res[4])

    #Muestra el paso a paso del recorrido de la cadena(Por consola)
    def probarCadena(self):
        cadena = eg.enterbox(msg='Ingrese Cadena: ',
                                  title='Control: Cadenas ',
                                  default='', strip=True,
                                  image=None)
        pc = probadorDeCadena.probadorDeCadena(self.alfabeto,self.estados,
                                               self.trans,self.inicial,self.terminal)
        estado = pc.comprobarCadena(cadena)
        if estado:
            eg.msgbox(msg='La cadena '+cadena+' es válida',
                      title='Probar Cadenas',
                      ok_button='Aceptar',
                      image=None)
        else:
            eg.msgbox(msg='Cadena no válida',
                      title='Probar Cadenas',
                      ok_button='Aceptar',
                      image=None)
                      
    #Grafica el automata de aqui para abajo                      
    def ingresarGraficoManual(self):
        self.ventana.destroy()
        graficarManualmente.Ventana()


    def generarDigraphdesdeER(self):
        self.generarDigraph()
        print(self.estados)
        print(self.inicial)
        print(self.terminal)
        print(self.trans)
        print(self.alfabeto)
        self.graficar()
        img = Image.open("Digraph.gif")
        img = img.resize((1200, 500), Image.ANTIALIAS)
        img = img.save("Digraph.gif")
        img1 = PhotoImage(master=self.ventana, file="Digraph.gif")
        Label(master=self.ventana, image=img1).place(x=0, y=0)
        Label(self.ventana, text=self.posfija, font=("Times Roman", 9), fg="Red").place(x=10, y=10)

        self.ventana.mainloop()

    def generarDigraphdesdeAUT(self, estados,inicial,final,trans,alf):

        self.estados = estados
        self.inicial = inicial
        self.terminal = final
        self.trans = trans
        self.alfabeto = alf
        self.graficar()

        img = Image.open("Digraph.gif")
        img = img.resize((1200, 500), Image.ANTIALIAS)
        img = img.save("Digraph.gif")
        img1 = PhotoImage(master=self.ventana, file="Digraph.gif")
        Label(master=self.ventana, image=img1).place(x=0, y=0)
        Label(self.ventana, text="Pila REGEX: "+str(self.posfija), font=("Times Roman", 9), fg="Red").place(x=10, y=10)
        self.ventana.mainloop()

    def ingresarExpresionRegular(self):
        self.ventana.destroy()
        er = ExpresionRegular()
        er.crear()

    def metodo(self):
        ER = AutomataaExpresionRegular.AutomataaExpresionRegular(self.alfabeto,self.estados,self.trans,self.inicial,self.terminal)
        ER.prueba()
        ER.prueba2()

    def graficar(self):
        draw(self.alfabeto, self.estados, self.inicial, self.trans, self.terminal)
        check_call(['dot', '-Tpng', 'Digraph.gv', '-o', 'Digraph.gif'])


    def generarDigraph(self):
        self.pilaIni = Pila.Pila()
        self.pilaFin = Pila.Pila()
        for i in self.posfija:
            if(i in self.alfabeto):
                self.crearTupla(i)
            elif(i == (".")):
                self.concatenar()
            elif(i == ("+")):
                self.operadorsuma()
            elif(i == ("*")):
                self.operadorasterisco()
            elif(i == ("?")):
                self.operadorInterrogacion()
            elif(i == ("|")):
                self.operadorO()

        self.actualizarInicialyFinal()

    def operadorO(self):
        estado1 = "q" + str(len(self.estados))
        estado4 = "q" + str(len(self.estados) + 1)
        estado3 = self.pilaFin.sacarPenultimo()
        estado2 = self.pilaIni.sacarPenultimo()
        estado5 = self.pilaIni.extraer()
        estado6 = self.pilaFin.extraer()
        self.estados.append(estado1)
        self.estados.append(estado4)
        trans1 = (str(estado1), str(estado2), "λ")
        trans2 = (str(estado3), str(estado4), "λ")
        trans3 = (str(estado1), str(estado5), "λ")
        trans4 = (str(estado6), str(estado4), "λ")
        self.pilaIni.incluir(estado1)
        self.pilaFin.incluir(estado4)
        self.trans.append(trans1)
        self.trans.append(trans2)
        self.trans.append(trans3)
        self.trans.append(trans4)

    def operadorInterrogacion(self):
        estado1 = "q" + str(len(self.estados))
        estado2 = "q" + str(len(self.estados) + 1)
        estado3 = self.pilaIni.extraer()
        estado4 = self.pilaFin.extraer()
        self.estados.append(estado1)
        self.estados.append(estado2)
        trans1 = (str(estado1), str(estado3), "λ")
        trans3 = (str(estado4), str(estado2), "λ")
        trans4 = (str(estado1), str(estado2), "λ")
        self.pilaIni.incluir(estado1)
        self.pilaFin.incluir(estado2)
        self.trans.append(trans1)
        self.trans.append(trans3)
        self.trans.append(trans4)

    def operadorsuma(self):
        estado1 = "q" + str(len(self.estados))
        estado2 = "q" + str(len(self.estados) + 1)
        estado3 = self.pilaIni.extraer()
        estado4 = self.pilaFin.extraer()
        self.estados.append(estado1)
        self.estados.append(estado2)
        trans1 = (str(estado1), str(estado3), "λ")
        trans2 = (str(estado4), str(estado3), "λ")
        trans3 = (str(estado4), str(estado2), "λ")
        self.pilaIni.incluir(estado1)
        self.pilaFin.incluir(estado2)
        self.trans.append(trans1)
        self.trans.append(trans2)
        self.trans.append(trans3)

    def operadorasterisco(self):
        estado1 = "q" + str(len(self.estados))
        estado2 = "q" + str(len(self.estados) + 1)
        estado3 = self.pilaIni.extraer()
        estado4 = self.pilaFin.extraer()
        self.estados.append(estado1)
        self.estados.append(estado2)
        trans1 = (str(estado1), str(estado3), "λ")
        trans2 = (str(estado4), str(estado3), "λ")
        trans3 = (str(estado4), str(estado2), "λ")
        trans4 = (str(estado1), str(estado2), "λ")
        self.pilaIni.incluir(estado1)
        self.pilaFin.incluir(estado2)
        self.trans.append(trans1)
        self.trans.append(trans2)
        self.trans.append(trans3)
        self.trans.append(trans4)

    def actualizarInicialyFinal(self):
        for i in self.pilaIni.items:
            self.inicial.append(str(i))
        for i in self.pilaFin.items:
            self.terminal.append(str(i))

    def concatenar(self):
        trans1 = (str(self.pilaFin.sacarPenultimo()),str(self.pilaIni.extraer()),"λ")
        self.trans.append(trans1)

    def crearTupla(self,simbolo):
        #Crear Estados
        estado1 = "q"+str(len(self.estados))
        estado2 = "q"+str(len(self.estados)+1)
        #Insertar estados a lista
        self.estados.append(estado1)
        self.pilaIni.incluir(estado1)
        #Insertar estados a pila
        self.estados.append(estado2)
        self.pilaFin.incluir(estado2)
        #Crear tupla transiciones
        tupla = (str(estado1),str(estado2),str(simbolo))
        self.trans.append(tupla)

    def mayuscula(self,listastring):
        listaaux =[]
        for i in listastring:
            listaaux.append(i.upper())
        return listaaux

def draw(alfabeto, estados, inicio, trans, final):
    g = gv.Digraph(format='svg')
    g.graph_attr['rankdir'] = 'LR'
    g.node('ini', shape="point")
    for e in estados:
        if e in final:
            g.node(e, shape="doublecircle")
        else:
            g.node(e)
        if e in inicio:
            g.edge('ini',e)

    for t in trans:
        if t[2] not in alfabeto:
            return 0
        g.edge(t[0], t[1], label=str(t[2]))
    g.render(view=False)
