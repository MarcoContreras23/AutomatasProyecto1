from Clases import Automata, Estado, Enlace, Elemento
import Clases
import copy

"""
Autores: Marco Contreras, Camilo Gomez
Version: 14.5
"""

enlaces = {}
tmpA = None

def inicial(automata):

    global enlaces

    estados = automata.getEnlaces() #aqui se reemplaza por las transiciones

    for estado in estados:
        todos = []
        llave = estado.getDesde()
        for e in estados:
            if e.getDesde() == llave:
                nuevo = []
                nuevo.append(e.getHasta())
                nuevo.append(e.getValor())
                todos.append(nuevo)
        enlaces[llave] = todos


# Convertir automata ND lambda a AFD
def convertirAFND(automata):
    nuevosEstados = {}
    nuevasUniones = []
    nuevoInicial = None
    nuevoFinal = []
    respuesta = []

    letra = ""
    abecedario = ['q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a', 'Z', 'Y', 'X',
                  'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D',
                  'C', 'B', 'A']
    textos = []
    texto = ""
    global enlaces
    inicial(automata)

    primero = clausura(automata.getEstadoInicial())

    if primero is not None:
        letra = abecedario.pop()
        letra2 = ""
        texto = "Cε(" + str(automata.getEstadoInicial().getId()) + ") = " + pasarS(primero) + " = " + letra
        textos.append(texto)
        nuevoInicial = letra
        nuevosEstados[letra] = primero
        pila = []
        pila.append(primero)
        alf = automata.getAlfabeto()
        alf = sorted(alf)

        while len(pila) >= 1:
            posibles = pila.pop()
            if len(abecedario) > 0:
                for e in nuevosEstados:
                    opc = nuevosEstados.get(e)
                    if opc == posibles:
                        letra = e
                        break
                for caracter in alf:
                    if caracter != 'λ':
                        texto = ""
                        mover = mover1(posibles, caracter)
                        if mover is not None:
                            texto = "irA(" + letra + "," + caracter + ")" + " = " + "Cε(mover(" + letra + "," + caracter + "))" + " = Cε(" + pasarS(
                                mover) + ") = "
                            nuevo = []
                            for e in mover:
                                nuevo1 = clausura(e)
                                if nuevo1 is not None:
                                    for e in nuevo1:
                                        nuevo.append(e)
                            if nuevo is not None or len(nuevo) >= 1:
                                esta = False
                                quien = ""
                                for e in nuevosEstados:
                                    opc = nuevosEstados.get(e)
                                    if opc == nuevo:
                                        esta = True
                                        quien = e
                                        break
                                if esta:
                                    nuevasUniones.append([letra, quien, caracter])
                                    texto += pasarS(nuevo) + " = " + quien
                                else:
                                    letra2 = abecedario.pop()
                                    nuevosEstados[letra2] = nuevo
                                    nuevasUniones.append([letra, letra2, caracter])
                                    lol = pasarS(nuevo) + " = " + letra2
                                    texto += lol
                                    pila.insert(0, nuevo)
                            else:
                                texto += "ø "
                        else:
                            texto = "irA(" + letra + "," + caracter + ")" + " = " + "Cε(mover(" + letra + "," + caracter + "))" + " = ø"
                        textos.append(texto)
            else:
                break
        if len(abecedario) > 0:
            retorno = [nuevosEstados, nuevasUniones, nuevoInicial, nuevoFinal, textos]
            for e in nuevosEstados:
                opc = nuevosEstados.get(e)
                for o in opc:
                    if o in automata.getEstadoFinal():
                        nuevoFinal.append(e)
                        break
        else:
            retorno = None
        return retorno
    else:
        return None

def mover1(estados, etiqueta):
    global enlaces
    retorno = []

    for estado in estados:
        enlaces1 = enlaces.get(estado)
        if enlaces1 is not None:
            if len(enlaces) >= 1:
                for e in enlaces1:
                    if e[1] == etiqueta:
                        retorno.append(e[0])
        else:
            pass
    if retorno is not None and len(retorno) >= 1:
        return retorno
    else:
        return None


def clausura(estado):
    primero = []
    pila = []
    pila.append(estado)

    while len(pila) >= 1:
        estado = pila.pop()
        primero.append(estado)
        posibles = enlaces.get(estado)
        if posibles is not None:
            if len(posibles) >= 1:
                for e in posibles:
                    if e[1] == 'λ':
                        pila.append(e[0])
    if primero is not None and len(primero) >= 1:
        return primero
    else:
        return None

def pasarS(estados):
    nuevo = "[ "

    for e in estados:
        nuevo += e.getId() + " "
    nuevo += "]"
    return nuevo


# Probar cadenas
def probarEntrada(automata, cadena):
    if automata.getTipo() == "D":
        inicial(automata)

        estadoF = probar_Determinista(automata.getEstadoInicial(), cadena)
        if estadoF in automata.getEstadoFinal():
            return True
        elif estadoF is None:
            return False
        else:
            return False

    if automata.getTipo() == "ND":
        inicial(automata)
        estadoF = probar_NDeterminista(automata.getEstadoInicial(), cadena)
        retorno = True
        esta = False
        if estadoF is None:
            retorno = False
        else:
            if len(estadoF) >= 1:
                for e in estadoF:
                    if e in automata.getEstadoFinal():
                        esta = True
                        break
                if esta == False:
                    retorno = False
            else:
                retorno = False
        return retorno
    if automata.getTipo() == "NDL":
        retorno = True
        convertir = convertirAFND(automata)
        if convertir is not None:
            nuevoA = Automata.Automata()
            nuevoA.setEstadoInicial(convertir[2])
            nuevoA.setAlfabeto(automata.getAlfabeto())
            estados = convertir[0]
            for e in estados:
                nuevoA.agregarEstado(estados[e])
            finales = convertir[3]
            for e in finales:
                nuevoA.agregarEstadoFinal(finales[e])
            enlacesN = convertir[1]
            for e in enlacesN:
                nuevoA.agregarEnlace(enlacesN[e])
            inicial(nuevoA)
            estadoF = probar_Determinista(nuevoA.getEstadoInicial(), cadena)
            if estadoF is None:
                retorno = False
            elif estadoF in nuevoA.getEstadoFinal():
                retorno = True
            else:
                retorno = False
        else:
            retorno = False

        return retorno

def probar_Determinista(estado, cadena):
    global enlaces

    if len(cadena) == 1:
        if estado is None:
            return None

        posibles = []
        encontro = True
        posibles = enlaces.get(estado)

        if posibles is None:
            encontro = False
            return None
        else:
            for p in posibles:
                if p[1] == cadena:
                    encontro = False
                    return p[0]
                    break
        if encontro:
            return None
    else:
        return probar_Determinista(probar_Determinista(estado, cadena[0:len(cadena) - 1]), cadena[len(cadena) - 1])


def probar_NDeterminista(estado, cadena):

    guardar = None
    estadosActual = [estado]

    for c in cadena:
        estadosActual = mover1(estadosActual, c)
        if estadosActual is None:
            estadosActual = None
            break
    if estadosActual is not None:
        if len(estadosActual) >= 1:
            return estadosActual
    else:
        return None


# Convertir automata a ER
def convertir_a_ER(automata):
    inicial(automata)
    convertible(automata)
    convetirGTG(automata)
    return obtenerExpreGTG(automata)


def obtenerExpreGTG(automata):
    ii = getII(automata)
    ij = getIJ(automata)
    jj = getJJ(automata)
    ji = getJI(automata)
    return expreFinal(ii, ij, jj, ji)


def expreFinal(ii, ij, jj, ji):
    tmp = concatenar(asterisco(ii), concatenar(ij, concatenar(asterisco(jj), ji)))
    tmp2 = concatenar(asterisco(ii), concatenar(ij, asterisco(jj)))
    expresion = concatenar(asterisco(tmp), tmp2)
    return expresion


def getJI(automata):
    for e in automata.getEnlaces():
        if e.getDesde() == automata.getEstadoFinal()[0] and e.getHasta() == automata.getEstadoInicial():
            return e.getValor()

def getJJ(automata):
    inicial = automata.getEstadoFinal()[0]
    for e in automata.getEnlaces():
        if e.getDesde() == inicial and e.getHasta() == inicial:
            return e.getValor()

def getIJ(automata):
    for e in automata.getEnlaces():
        if e.getDesde() == automata.getEstadoInicial() and e.getHasta() == automata.getEstadoFinal()[0]:
            return e.getValor()

def getII(automata):
    inicial = automata.getEstadoInicial()
    for e in automata.getEnlaces():
        if e.getDesde() == inicial and e.getHasta() == inicial:
            return e.getValor()

def convertible(automata):
    global tmpA

    if len(automata.getEstadoFinal()) > 1:
        temp = automata.getEstadoFinal()
        nuevoF = Estado.Estado("f", (1, 1))
        if automata.getEstadoInicial() in temp:
            tmpA = True
        for e in temp:
            automata.agregarEnlace(Enlace.Enlace(e, nuevoF, "λ", "normal1"))
        automata.setEstadoFinal([nuevoF])
        automata.agregarEstado(nuevoF)
    if len(automata.getEstadoFinal()) == 1:
        if automata.getEstadoInicial() == automata.getEstadoFinal()[0]:
            tmpA = True
            nuevoF = Estado.Estado("f", (1, 1))
            automata.agregarEnlace(Enlace.Enlace(automata.getEstadoInicial(), nuevoF, "λ", "normal1"))
            automata.setEstadoFinal([nuevoF])
            automata.agregarEstado(nuevoF)
    estados = automata.getEstado()
    enlaces = automata.getEnlaces()

    existen = {}

    for e in estados:
        lista = []
        for e1 in enlaces:
            if e1.getDesde() == e:
                lista.append(e1.getHasta())
        existen[e] = lista

    for e in estados:
        esta = existen.get(e)
        for e1 in estados:
            if e1 not in esta:
                nuevo = Enlace.Enlace(e, e1, "ø", "normal1")
                automata.agregarEnlace(nuevo)

def convetirGTG(automata):
    final = automata.getEstadoFinal()[0]
    inicial = automata.getEstadoInicial()
    estados = automata.getEstado()
    cont = 0

    while len(estados) > 2:
        e = estados[cont]
        if e != final and e != inicial:
            lista = getTrans_E_Removible(e, automata)
            removerEstado(e, lista, automata)
            estados = automata.getEstado()
            cont = 0
        cont += 1

def removerEstado(estado, lista, automata):
    automata.getEstado().remove(estado)
    if estado in automata.getEstadoFinal():
        automata.getEstadoFinal().remove(estado)
    if estado == automata.getEstadoInicial():
        automata.setEstadoInicial(None)
    automata.setEnlaces(lista)


def getTrans_E_Removible(estado, automata):

    lista = []
    id = estado.getId()
    estados = automata.getEstado()

    if esRemovible(estado, automata):
        return None
    for e in estados:
        p = e.getId()
        if p != id:
            for e1 in estados:
                p1 = e1.getId()
                if p1 != id:
                    exp = getExpresion(p, p1, id, automata)
                    lista.append(getTransicionExpre(p, p1, exp, automata))
    return lista


def getTransicionExpre(p, q, exp, automata):

    desdeE = None
    hastaE = None

    for e in automata.getEstado():
        if desdeE is not None and hastaE is not None:
            break
        if e.getId() == p:
            desdeE = e
        if e.getId() == q:
            hastaE = e
    nuevo = Enlace.Enlace(desdeE, hastaE, exp, "normal1")
    return nuevo


def esRemovible(estado, automata):

    if estado == automata.getEstadoFinal()[0] or estado == automata.getEstadoInicial():
        return True
    else:
        return False

def getExpresion(p, q, k, automata):

    desdeE = None
    hastaE = None
    removerE = None

    for e in automata.getEstado():
        if desdeE is not None and hastaE is not None and removerE is not None:
            break
        if e.getId() == p:
            desdeE = e
        if e.getId() == q:
            hastaE = e
        if e.getId() == k:
            removerE = e
    pq = getExpresion_entre_estados(desdeE, hastaE, automata)
    pk = getExpresion_entre_estados(desdeE, removerE, automata)
    kk = getExpresion_entre_estados(removerE, removerE, automata)
    kq = getExpresion_entre_estados(removerE, hastaE, automata)
    tmp1 = asterisco(kk)
    tmp2 = concatenar(pk, tmp1)
    tmp3 = concatenar(tmp2, kq)
    label = o(pq, tmp3)
    return label

def getExpresion_entre_estados(desde, hasta, automata):

    enlaces = automata.getEnlaces()
    valor = ""

    for e in enlaces:
        if e.getDesde() == desde and e.getHasta() == hasta:
            valor = e.getValor()
    return valor


def o(exp1, exp2):

    if exp1 == "ø":
        return exp2
    if exp2 == "ø":
        return exp1
    if exp1 == "" and exp2 == "":
        return ""
    if exp1 == "":
        exp1 = "λ"
    if exp2 == "":
        exp2 = "λ"
    if exp1 == exp2:
        return exp1
    return exp1 + "|" + exp2

def concatenar(exp1, exp2):

    global tmpA
    if exp1 == "ø" or exp2 == "ø":
        return "ø"
    if exp1 == "":
        return exp2
    if exp2 == "":
        return exp1
    if exp1 == "λ":
        return exp2
    if exp2 == "λ":
        return exp1
    if len(otro(exp1)) > 1:
        exp1 = addParen(exp1)
    if len(otro(exp2)) > 1:
        exp2 = addParen(exp2)
    if tmpA:
        if exp1[len(exp1) - 1] == "*" and exp2[len(exp2) - 1] != "*":
            comparar2 = exp1[:len(exp1) - 1]
            igual = True
            cont = 0
            for c in comparar2:
                if c != exp2[cont]:
                    igual = False
                    break
                cont += 1
            if igual:
                return exp1
        if exp2[len(exp2) - 1] == "*" and exp1[len(exp1) - 1] != "*":
            comparar2 = exp2[:len(exp2) - 1]
            igual = True
            cont = 0
            for c in comparar2:
                if c != exp1[cont]:
                    igual = False
                    break
                cont += 1
            if igual:
                return exp2
    return exp1 + exp2

def asterisco(exp):

    if exp == "ø" or exp == "":
        return ""
    if len(otro(exp)) > 1 or len(otro2(exp)) > 1:
        exp = addParen(exp)
    elif exp[len(exp) - 1] == "*":
        return exp
    return exp + "*"

def addParen(exp):
    return "(" + exp + ")"

def otro(exp):

    lista = []
    start = 0
    nivel = 0
    cont = 0

    for c in exp:
        if c == "(":
            nivel += 1
        if c == ")":
            nivel -= 1
        if c == "|":
            if nivel == 0:
                lista.append(delamba(exp[start: cont]))
                start = cont + 1
        cont += 1
    lista.append(delamba(exp[start:]))

    return lista

def otro2(exp):

    lista = []
    start = 0
    nivel = 0
    cont = 0

    for c in exp:
        if c == ")":
           nivel -= 1
        else:
            if c == "(":
                nivel += 1
            if (c == "(" and nivel == 1) or (nivel == 0):
                if c == "|":
                    print("error")
                if c != "*":
                    if (cont != 0):
                        lista.append(delamba(exp[start:cont]))
                        start = cont
        cont += 1
    lista.append(delamba(exp[start:]))
    return lista


def delamba(exp):

    if exp == "λ":
        return ""
    else:
        return exp

def inicial1(automata):
    global enlaces

    estados = automata.getEnlaces()

    for estado in estados:

        todos = []

        llave = estado.getDesde()

        for e in estados:

            if e.getDesde() == llave:
                nuevo = []
                nuevo.append(e.getHasta())
                nuevo.append(e.getValor())
                todos.append(nuevo)

        enlaces[llave] = todos

# Minimizar por los 2 metodos
def minimizar(automata, metodo):

    if metodo == "1":
       eliminarNoEntrada(automata)
    inicial1(automata)
    automataRetorno = copy.deepcopy(automata)
    if metodo == "1":
        matriz = []
        fila = len(automata.getEstado()) - 1
        i = 0
        dx = 1

        while i < fila:
            estado = automata.getEstado()[i]
            j = fila
            while j >= dx:
                matriz.append(Elemento.ElementoM(estado, automata.getEstado()[j], " "))
                j -= 1
            dx += 1
            i += 1
        finales = automata.getEstadoFinal()
        for e in matriz:
            if e.getF() in finales:
                if e.getC() not in finales:
                    e.setValor("X")
                    e.setCaracter("SI")
            if e.getC() in finales:
                if e.getF() not in finales:
                    e.setValor("X")
                    e.setCaracter("SI")
        tmp = []
        for e in matriz:
            if e.getCaracter() != "SI":
                for c in automata.getAlfabeto():
                    if c != "λ":
                        tmp2 = mover1([e.getF()], c)
                        tmp3 = mover1([e.getC()], c)
                        terminar = True
                        if (tmp2 is not None) and (tmp3 is not None):
                            for i in tmp2:
                                if terminar:
                                    for j in tmp3:
                                        if (i in finales) and (j not in finales):
                                            posible = Elemento.ElementoM(i, j, "SI")
                                            posible.setCaracter(c)
                                            e.nuevoValor(posible)
                                            e.setCaracter("SI")
                                            terminar = False
                                            break
                                        elif (j in finales) and (i not in finales):
                                            posible = Elemento.ElementoM(i,j, "SI")
                                            posible.setCaracter(c)
                                            e.nuevoValor(posible)
                                            e.setCaracter("SI")
                                            terminar = False
                                            break
                                else:
                                    break
                            if terminar:
                                posible = Elemento.ElementoM(tmp2[0], tmp3[0], "NO")
                                posible.setCaracter(c)
                                e.nuevoValor(posible)
        faltan = []
        for e in matriz:
            if e.getCaracter() == "E":
                faltan.append(e)
        if len(faltan) == 0:
            return None
        estan = []
        for e in matriz:
            if e.getCaracter() == "SI":
                estan.append(e)
        cambio = True
        cambio2 = False

        while cambio:
            cont1 = 0
            cambio2 = False
            removerE = []
            while len(faltan) >= 1 and cont1 < len(faltan):
                pos = faltan[cont1].getValores()
                for p in pos:
                    for i in estan:
                        if p.getC() == i.getC() and p.getF() == i.getF():
                            cambio2 = True
                            nuevoE = faltan[cont1]
                            nuevoE.setCaracter("SI")
                            estan.append(nuevoE)
                            removerE.append(nuevoE)
                            break
                        elif p.getC() == i.getF() and p.getF() == i.getC():
                            cambio2 = True
                            nuevoE = faltan[cont1]
                            nuevoE.setCaracter("SI")
                            estan.append(nuevoE)
                            removerE.append(nuevoE)
                            break
                    if cambio2:
                        break
                cont1 += 1

            for e in removerE:
                faltan.remove(e)
            if cambio2 == False:
                cambio = False
            if len(faltan) <= 0:
                break
        conjuntos = []
        for e in matriz:
            if e.getCaracter() == "E":
                e.setCaracter("NO")
                c1 = set()
                c1.add(e.getC())
                c1.add(e.getF())
                conjuntos.append(c1)
        repetir = True

        while repetir:
            cont = 0
            repetir1 = False
            comenzar = False
            while cont < len(conjuntos):
                if comenzar:
                    break
                tmp1 = conjuntos[cont]
                cont2 = 0
                while cont2 < len(conjuntos):
                    tmp2 = conjuntos[cont2]
                    if tmp1 != tmp2:
                        interseccion = tmp1.intersection(tmp2)
                        if interseccion is not None:
                            if len(interseccion) >= 1:
                                nuevo = set()
                                for e in tmp1:
                                    nuevo.add(e)
                                for e in tmp2:
                                    nuevo.add(e)
                                conjuntos.remove(tmp1)
                                conjuntos.remove(tmp2)
                                conjuntos.append(nuevo)
                                comenzar = True
                                repetir1 = True
                                break
                    cont2 += 1
                cont += 1
            if repetir1 == False:
                repetir = False

        estados = automata.getEstado()
        alfa = automata.getAlfabeto()
        nuevosEstados = []

        for e in conjuntos:
            inicial1(automata)
            final = True
            inicial = True
            enlaces = set()
            label = ""
            for i in e:
                label +=  i.getId()  + ","
            label = label[:len(label) - 1]
            nuevoE = Estado.Estado(label, (0, 0))
            for i in e:
                if i in automata.getEstadoFinal() and final:
                    final = False
                    automata.agregarEstadoFinal(nuevoE)
                if i == automata.getEstadoInicial() and inicial:
                    inicial = False
                    automata.setEstadoInicial(nuevoE)
            automata.agregarEstado(nuevoE)
            for e1 in estados:
                for c in alfa:
                    tmp = mover1([e1],c)
                    if tmp is not None:
                        tmp = tmp[0]
                        if e1 in e and tmp in e:
                            if verificarEn(nuevoE,nuevoE,c , enlaces):
                              enlaces.add(Enlace.Enlace(nuevoE, nuevoE, c, "mismo"))
                        elif e1 in e and tmp not in e:
                            if verificarEn(nuevoE, tmp, c, enlaces):
                             enlaces.add(Enlace.Enlace(nuevoE, tmp, c, "mismo"))
                        elif tmp in e:
                            if verificarEn(e1, nuevoE, c, enlaces):
                              enlaces.add(Enlace.Enlace(e1, nuevoE, c, "mismo"))
            removerEn = []
            for e4 in enlaces:
                automata.agregarEnlace(e4)
            for i in e:
                for k in automata.getEnlaces():
                    if k.getDesde() == i or k.getHasta() == i:
                        removerEn.append(k)

            for c in removerEn:
                try:
                     automata.getEnlaces().remove(c)
                except:
                    pass
            for i in e:
                if i in automata.getEstadoFinal():
                    automata.getEstadoFinal().remove(i)
                automata.getEstado().remove(i)
        retorno = [corregirEnlaces(automata), matriz, automataRetorno]
        return retorno

    if metodo == "2":
        alfabeto = ['x', 'y','w','z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's' , 't', 'u', 'v']
        respuesta = []
        respuestaT = "  " + alfabeto[0] + " = {"
        conjuntos = {}
        finales = automata.getEstadoFinal()
        normales = []
        temp = alfabeto[1] + " = {"
        for estado in automata.getEstado():
            if estado not in finales:
                normales.append(estado)
                respuestaT += " " + estado.getId() + ","
            else:
                temp += " " + estado.getId() + ","

        temp = temp[:len(temp) - 1]
        temp += "}"
        respuestaT = respuestaT[:len(respuesta) - 1]
        respuestaT += "}  " + temp
        respuesta.append(respuestaT)
        conjuntos[alfabeto[0]] = normales
        conjuntos[alfabeto[1]] = finales
        alabetoA = automata.getAlfabeto()
        temp = True

        while temp:
            nuevoConjunto = {}
            sustituir = {}
            tmp2 = ""
            for llave , estados in conjuntos.items():
                conjuntoTemp = {}
                for estado in estados:
                    tmp = ""
                    for caracter in alfabetoA:
                        mover = mover1([estado], caracter)
                        if mover is not None:
                            if len(mover) >= 1:
                                for llaveE, estadosE in conjuntos.items():
                                    if mover[0] in estadosE:
                                        tmp += llaveE
                                        break
                    if len(conjuntoTemp) == 0:
                         conjuntoTemp[tmp] = [estado]
                    else:
                        llaves = conjuntoTemp.keys()
                        if tmp in llaves:
                            d = conjuntoTemp[tmp]
                            d.append(estado)
                            conjuntoTemp[tmp] = d
                        else:
                            conjuntoTemp[tmp] = [estado]

                borrarE = []
                nuevosI = []

                for e in conjuntoTemp:
                    if e in nuevoConjunto.keys():
                        borrarE.append(e)
                        nuevosI.append([e + " ", conjuntoTemp.get(e) ])
                for element in borrarE:
                    del conjuntoTemp[element]
                for ele in nuevosI:
                    conjuntoTemp[ele[0]] = ele[1]

                nuevoConjunto.update(conjuntoTemp)

            cont = len(conjuntos)
            conjuntoLen = len(conjuntos)

            for llaveI , estadosI in nuevoConjunto.items():
                estadoI = estadosI[0]
                if len(conjuntos) >= 1:
                    esta = True
                    eliminar = []
                    for llaveP, estadosP in conjuntos.items():
                        if estadoI in estadosP:
                            eliminar.append(llaveP)
                            sustituir[llaveP] = estadosI
                            esta = False
                            break
                    for e in eliminar:
                        del conjuntos[e]
                    if esta:
                        sustituir[alfabeto[cont]] = estadosI
                        cont += 1
                else:
                    sustituir[alfabeto[cont]] = estadosI
                    cont += 1
            if len(sustituir) > conjuntoLen:
                for llavet in sustituir:
                    estates = sustituir.get(llavet)
                    tmp2 +=  "  " + llavet + " = {"
                    for estate in estates:
                        tmp2 += " " + estate.getId() + ","
                    tmp2 = tmp2[:len(tmp2) - 1]
                    tmp2 += "}"
                respuesta.append(tmp2)
                conjuntos = sustituir
            else:
                temp = False

        inicialR = ""
        final = []
        enlaces = []
        estadosR = []
        encontro = True
        for llave, estados in sustituir.items():
            estadosR.append(llave)
            for e in estados:
                if encontro:
                    if e == automata.getEstadoInicial():
                        inicialR = llave
                        encontro = False
                elif e in automata.getEstadoFinal():
                    if llave not in final:
                       final.append(llave)

        for llave, estados in sustituir.items():
            estado = estados[0]
            for c in alfabetoA:
               mover = mover1([estado] , c)
               if mover is not None:
                   if len(mover) >= 1:
                       for llaveT, estadosT in sustituir.items():
                           if mover[0] in estadosT:
                               enlaces.append([llave,llaveT,c])
                               break
        retorno = [estadosR,enlaces,inicialR,final, respuesta]
        return retorno

def verificarEn(e1, e2 ,c, estados):

    esta = True
    for e in estados:
        if e.getDesde() == e1 and e.getHasta() == e2 and e.getValor() == c:
            esta = False
            break
    return esta

def corregirEnlaces(automata):

    nuevo = []
    cont = 0

    while cont < len(automata.getEnlaces()):
        e = automata.getEnlaces()[cont]
        esta = 0
        label = ""
        elimino = False
        eliminar = []
        desde = e.getDesde()
        hasta = e.getHasta()

        for e1 in automata.getEnlaces():
            if e1.getDesde() == desde and e1.getHasta() == hasta:
                esta += 1
                label += e1.getValor() + ","
                eliminar.append(e1)
        if esta > 1:
            automata.agregarEnlace(Enlace.Enlace(desde,hasta,label[:len(label) - 1],"mismo"))
            elimino = True
            for i in eliminar:
                automata.getEnlaces().remove(i)
        if elimino :
          cont = 0
        else:
            cont += 1
    return automata

def eliminarNoEntrada(automata):

    lista = []
    eliminar = True
    for e in automata.getEstado():
        eliminar = True
        if e != automata.getEstadoInicial():
            for e1 in automata.getEnlaces():
                if e1.getHasta() == e:
                    eliminar = False
                    break
            if eliminar:
                lista.append(e)
    for e in lista:
        remover = []
        for e1 in automata.getEnlaces():
            if e1.getDesde() == e or e1.getHasta() == e:
                remover.append(e1)
        for r in remover:
            automata.getEnlaces().remove(r)
        if e in automata.getEstadoFinal():
            automata.getEstadoFinal().remove(e)
        if e == automata.getEstadoInicial():
            automata.setEstadoInicial(None)
        automata.getEstado().remove(e)



