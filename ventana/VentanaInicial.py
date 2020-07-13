from tkinter import *
import convertirERaPostOrden 
import automa
import graficarManualmente

"""
Autores: Marco Contreras
Version 4.5
"""

class ExpresionRegular():
    def __init__(self):
        self.ventana2 = Tk()
        self.expresion = StringVar(self.ventana2)
        self.alfabeto = StringVar(self.ventana2)
        self.caracteres = ["(",")","*","+","?","|","."]
        
    def crear(self):
        
        self.ventana2.title("Expresion Regular")
        self.ventana2.geometry('330x220')
        self.ventana2.resizable(False, False)
        
        #Entrada Alfabeto
        Label(self.ventana2,text="Ingrese el alfabeto").place(x = 40, y = 20)
        Label(self.ventana2,text="Ejemplo= a,b,h,j,1,0  ").place(x = 40, y = 40)
        textoentrada = Entry(self.ventana2,textvariable=self.alfabeto).place(x = 40,y = 60)
        Label(self.ventana2,text="(Cada símbolo separado por comas)").place(x = 40, y = 80)
        Label(self.ventana2,text="_____________________________________________").place(x = 30, y = 100)

        #Entrada ER
        Label(self.ventana2,text="Expresión Regular:").place(x = 40, y = 120)
        textoentrada = Entry(self.ventana2,textvariable=self.expresion,width=40).place(x = 40,y = 140)

        #Llamada el metodo CrearAutomata para validar
        Button(self.ventana2,text="Crear Autómata", command = self.crearAutomata).place(x=50, y=180)
        
        self.ventana2.mainloop()

    #Metodo del boton crear automata que valida si el ER concuerda con la Expresion
    def crearAutomata(self):
        alf = self.alfabeto.get()
        exp = self.expresion.get()
        auxexp = self.expresion.get()

        if(self.validar(alf,exp)):
            ER = convertirERaPostOrden.ERaPF(auxexp)
            g = automa.GraficadoraAutomatas(ER,alf.split(","))
            self.ventana2.withdraw()
            g.crear()
            g.generarDigraphdesdeER()
        else:
            Label(self.ventana2,text="Revise el alfabeto y la expresion",font=("Times Roman",9),fg="Red").place(x = 40, y = 160)

    #Validad que el alfabeto coincida con la expresion
    def validar(self,alfabeto,expresion):
        
        estado = False
        alf = alfabeto.split(",")      
        caracteresoriginal = self.caracteres
        self.caracteres.extend([element for element in alf if element not in self.caracteres])
   
        for i in expresion:
            for j in self.caracteres:
                if i == j:
                    estado = True         
            if estado == False:
                self.caracteres = caracteresoriginal
                return False
            estado = False
        return True

class dialogo():

    def __init__(self):
        self.ventana = Tk()

    #Boton que llama el metodo insertarExpresion
    def ER(self):
        self.ventana.withdraw()
        self.insertarExpresionRegular()
        
    def insertarExpresionRegular(self):
        e = ExpresionRegular()
        e.crear()
    #boton para llamar la clase expresion regular e ingresar datos de la expresión regular
    def AU(self):
        self.ventana.withdraw()
        graficarManualmente.Ventana()
    # Ventana inicial
    def crear(self):
        
        self.ventana.title("Proyecto Automatas")
        self.ventana.geometry('200x200')
        self.ventana.resizable(False, False)

        Label(text='INGRESAR:').place(x=70, y=30)
        Button(text="Expresion Regular", command = self.ER).place(x=45, y=70)
        #Button(text="Automata (Grafico)", command = self.AU).place(x=40, y=120)
        self.ventana.mainloop()
        
if __name__ == '__main__':
    n = dialogo()
    n.crear()
