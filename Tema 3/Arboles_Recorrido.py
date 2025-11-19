#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Tree:
    def __init__(self, data):
        self.children = []
        self.data = data

a = Tree("A")
b = Tree("B")
c = Tree("C")
root = Tree("root")
root.children.append(a)
root.children.append(b)
root.children.append(c)


a1=Tree("A1")
a2=Tree("A2")
root.children[0].children.append(a1)
root.children[0].children.append(a2)


b1=Tree("B1")
b2=Tree("B2")
root.children[1].children.append(b1)
root.children[1].children.append(b2)

c1=Tree("C1")
c2=Tree("C2")
root.children[2].children.append(c1)
root.children[2].children.append(c2)

'''def recorrerArbolpre(arbol):
    print(arbol.data)
    for i in arbol.children:
        recorrerArbolpre(i)
recorrerArbolpre(a)

#metodo recursivo para imprimir los nodos y recorerlos en profundidad profundidad (preorden)
def recorrido_profundidad(nodo):
    print(nodo.data)
    for child in nodo.children:
        recorrido_profundidad(child)
recorrido_profundidad(root)
print("")
print("")
# recorrido  postorden (recursivo)
def recorrido_postorden(nodo):
    for child in nodo.children:
        recorrido_postorden(child)
    print(nodo.data)
recorrido_postorden(root)
print("")
print("")
#recorrido inorden (recursivo)
def recorrido_inorden(nodo):
    if len(nodo.children) > 0:
        recorrido_inorden(nodo.children[0])
    print("recorrido in order",nodo.data)
    for child in nodo.children[1:]:
        recorrido_inorden(child)
recorrido_inorden(root)

#metodo iterativo para imprimir los nodos en amplitud
def recorrido_amplitud(nodo):
    cola = [nodo]
    while cola:
        actual = cola.pop(0)
        print(actual.data)
        for child in actual.children:
            cola.append(child)
recorrido_amplitud(root)'''

# Ejercicio de backtrackin, ¿Cuántas posibilidades tenemos de sumar un número entero positivo en concreto?


def backtrakking(objetivo,solucion_parcial, soluciones, paso):
    exito = False # exito indica que cuando sea true mo va a buscar mas soluciones
    opciones = list(range(1, objetivo))
    i=0
    while i<len(opciones) and not exito:
        opcion = opciones[i]
        #extraer la siguiente opcion
        suma = sum(solucion_parcial)+opciones[i]
        if suma <= objetivo: # es aceptable la solucion?
            solucion_parcial.append(opcion)
            if suma == objetivo:
                #exito = True
                #anoto paso
                soluciones.append(solucion_parcial.copy()) # guardo solucion encontrada (copia)
            else:
                 #backtrakking(objetivo,solucion_parcial, soluciones, paso+1)
                 exito = backtrakking(objetivo,solucion_parcial, soluciones, paso+1)
            # desanoto paso
            solucion_parcial.pop() # deshago la eleccion # elimina el ultimo añadido
        else:
            exito = False
        i+=1

    return exito


#creamos el array de soluciones
solucion_parcial=[]
soluciones=[]

backtrakking(4,solucion_parcial,soluciones,1)
for i in soluciones:
    print(i)
