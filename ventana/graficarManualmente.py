
from tkinter import messagebox
import pygame   
import sys
from pygame.locals import *
from tkinter import *
import easygui as eg
import automa


"""
Autores: Marco Contreras, Camilo Gomez
Version 4.0
"""

class InterfazAutomatas():
    def __init__(self):
        self.estados = []
        self.estadosObjetos = []
        self.transObjetos = []
        self.trans = []
        self.final = []
        self.inicial = []
        self.alfabeto = []
        self.estadoGraficacion = 1

    def dibujar(self, superficie):
        fuente = pygame.font.Font(None, 23)
        texto2 = fuente.render("Instrucciones", 0, (0, 0, 0))
        superficie.blit(texto2, (10, 10))
        texto2 = fuente.render("Presione el numero correspondiente para realizar el automata", 0, (0, 0, 0))
        superficie.blit(texto2, (10, 30))
        texto2 = fuente.render("1. Crear Estados", 0, (0, 0, 0))
        superficie.blit(texto2, (10, 60))
        texto2 = fuente.render("2. Crear transiciones", 0, (0, 0, 0))
        superficie.blit(texto2, (10, 80))
        texto2 = fuente.render("3. Seleccionar estado final", 0, (0, 0, 0))
        superficie.blit(texto2, (10, 100))
        texto2 = fuente.render("4. Seleccionar estado inicial", 0, (0, 0, 0))
        superficie.blit(texto2, (10, 120))
        texto2 = fuente.render("5. Terminar", 0, (0, 0, 0))
        superficie.blit(texto2, (10, 140))

        for estado in self.estadosObjetos:
            estado.dibujar(superficie)
        for trans in self.transObjetos:
            trans.dibujar(superficie)

    def realizarAccion(self,pos,estado):
        estado1trans = False
        estado2trans = False
        estadotrans = []
        if(self.estadoGraficacion == 1):
            if(estado == "Apretado"):
                nombreEstado = eg.enterbox(msg='Nombre del estado',
                                    title='Control: Estados',
                                    default='q'+str(len(self.estados)), strip=True,
                                    image=None)
                if(nombreEstado not in self.estados):
                    self.estados.append(nombreEstado)
                    self.estadosObjetos.append(estadoObjeto(pos[0],pos[1],nombreEstado))
                print("Estados"+str(self.estados))
        elif(self.estadoGraficacion == 2):
            if(estado == "Apretado"):
                self.pos1temp = pos
            elif(estado == "Desapretado"):
                self.pos2temp = pos
                for estado in self.estadosObjetos:
                    if(estado.rect.collidepoint(self.pos1temp)):
                        estado1trans = True
                        estadotrans.insert(0,estado.nombre)
                    if(estado.rect.collidepoint(self.pos2temp)):
                        estado2trans = True
                        estadotrans.insert(1,estado.nombre)

            if(estado1trans and estado2trans):
                nombreTrans = eg.enterbox(msg='Ingrese símbolo: ',
                                           title='Control: Transiciones ',
                                           default='λ', strip=True,
                                           image=None)
                if nombreTrans not in self.alfabeto:
                    self.alfabeto.append(nombreTrans)
                trans = (str(estadotrans[0]), str(estadotrans[1]), nombreTrans)
                self.trans.append(trans)
                self.transObjetos.append(transiciones(self.pos1temp,self.pos2temp,nombreTrans))
                print("Trans"+str(self.trans))
        elif(self.estadoGraficacion == 3):
            for estado in self.estadosObjetos:
                if(estado.rect.collidepoint(pos)):
                    nombreFinal = estado.nombre
                    estado.final = True
                    if nombreFinal in self.estados and nombreFinal not in self.final:
                        self.final.append(nombreFinal)
                        print("Final"+str(self.final))
        elif (self.estadoGraficacion == 4):
            for estado in self.estadosObjetos:
                if (estado.rect.collidepoint(pos)):
                    nombreInicial = estado.nombre
                    estado.inicial = True
                    if nombreInicial in self.estados and nombreInicial not in self.inicial:
                        self.inicial.append(nombreInicial)
                        print("Inicial" + str(self.inicial))
        elif(self.estadoGraficacion == 5):
            auto = automa.GraficadoraAutomatas([],[])
            auto.crear()
            pygame.quit()
            auto.generarDigraphdesdeAUT(self.estados, self.inicial, self.final, self.trans, self.alfabeto)

#Clase que asigna valores y dibuja las transiciones correspondientes

class transiciones():
    def __init__(self,pos1,pos2,nombre):
        pygame.sprite.Sprite.__init__(self)
        self.nombre = nombre
        self.pos1 = pos1
        self.pos2 = pos2
    def dibujar(self,superficie):
        fuente = pygame.font.Font(None, 23)
        texto1 = fuente.render("" + self.nombre, 0, (0, 0, 0))
        xtexto = (self.pos2[0] + self.pos1[0]) / 2
        ytexto = (self.pos2[1] + self.pos1[1]) / 2
        superficie.blit(texto1, (xtexto - 15, ytexto))
        pygame.draw.aaline(superficie,(100,100,100),self.pos1,self.pos2,1)

#Clase que asigna valores y dibuja los estados correspondientes
class estadoObjeto():
    def __init__(self,posX,posY,nombre):
        pygame.sprite.Sprite.__init__(self)
        self.nombre = nombre
        self.Imagen = pygame.image.load('C:\\Users\\marco\\OneDrive\\Documentos\\Automatas\\Automatasproyecto1\\ventana\Imagenes\\circulo.png')
        self.rect = self.Imagen.get_rect()
        self.rect.centerx = posX
        self.rect.centery = posY
        self.final = False
        self.inicial = False

    def dibujar(self,superficie):
        fuente = pygame.font.Font(None, 23)
        texto2 = fuente.render(""+self.nombre, 0, (0, 0, 0))
        superficie.blit(texto2, (self.rect.centerx-8, self.rect.centery-8))
        superficie.blit(self.Imagen, self.rect)
        if(self.inicial):
            pygame.draw.line(superficie,(100,100,100),(self.rect.centerx-50,self.rect.centery),
                             (self.rect.centerx-20,self.rect.centery),4)
            pygame.draw.line(superficie, (100, 100, 100), (self.rect.centerx - 30, self.rect.centery-10),
                             (self.rect.centerx - 30, self.rect.centery+10), 4)
        if (self.final):
            pygame.draw.circle(superficie,(100,100,100),(self.rect.centerx,self.rect.centery),28,3)

#Captura y validación del pintado manual del automata
def Ventana():

    pygame.init()

    #Crear ventana
    ventana = pygame.display.set_mode((1920, 1080))
    ImagenFondo = pygame.image.load("C:\\Users\\marco\\OneDrive\\Documentos\\Automatas\\Automatasproyecto1\\ventana\\Imagenes\\fondo-blanco.jpg")
    #Titulo de la ventana
    pygame.display.set_caption("Automata")
    interfaz = InterfazAutomatas()

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN,pygame.KEYUP):
                # obtiene el nombre de la tecla
                key_name = pygame.key.name(event.key)
                # convierte el nombre de la tecla en mayúsculas
                key_name = key_name.upper()
                # si alguna tecla es presionada
                if event.type == pygame.KEYDOWN:
                    # imprime en la consola la tecla presionada
                    if(str(format(key_name)) == "1"):
                        interfaz.estadoGraficacion = 1
                    elif(str(format(key_name)) == "2"):
                        interfaz.estadoGraficacion = 2
                    elif(str(format(key_name)) == "3"):
                        interfaz.estadoGraficacion = 3
                    elif(str(format(key_name)) == "4"):
                        interfaz.estadoGraficacion = 4
                    elif(str(format(key_name)) == "5"):
                        interfaz.estadoGraficacion = 5
                        interfaz.realizarAccion(0, "Desapretado")
            if event.type == pygame.MOUSEBUTTONDOWN:
                interfaz.realizarAccion(event.pos,"Apretado")
            if event.type == pygame.MOUSEBUTTONUP:
                interfaz.realizarAccion(event.pos,"Desapretado")
        pygame.display.update()
        ventana.blit(ImagenFondo, (0, 0))
        interfaz.dibujar(ventana)