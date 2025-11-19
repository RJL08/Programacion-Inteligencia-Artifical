from Arboles_Recorrido import solucion_parcial

#¿Dada una mochila con un peso máximo (peso_max) qué combinación de elementos
#(precio, peso) maximiza el valor total de la mochila?

def suma_peso(mochila):
    suma=0
    for peso,valor in mochila:
        suma+=peso
    return suma

def suma_valor(mochila):
    suma=0
    for peso,valor in mochila:
        suma+=valor
    return suma

def es_opcion_aceptable(mochila,objeto,peso_max):
    """
    :param mochila:
    :param objeto: tupla peso,valor
    :param peso_max:
    :return:
    """
    return suma_peso(mochila)+objeto[0] <= peso_max

def compara_mochila(mochila1, mochila2):
    """
    TODO
    :param mochila1:
    :param mochila2:
    :return: True si mochila1 tiene más valor que mochila2
    """

    return suma_valor(mochila1) > suma_valor(mochila2)

def copia_mochila(mochila_final, mochila):
    """
    TODO
    copia en mochila_final el contenido de mochila:
        vacía mochila_final y copia todos los elementos de mochila

    :param mochila_final:
    :param mochila:
    :return: None
    """
    mochila_final.clear()
    for peso, valor in mochila:
        mochila_final.append((peso, valor))

# backtracking
def optimiza_mochila(mochila,mochila_optima,items,peso_max):

    for i in range (0,len(items)):
        objeto = items[i]
        if es_opcion_aceptable(mochila,items[i],peso_max): #Me paso del peso??
            mochila.append(objeto) # anotar: añadir el elemento a la mochila y eliminarlo de los item

            items.pop(i) #Elimino el item de la lista de item

            #generar una nueva solución
            if compara_mochila(mochila, mochila_optima): #Si mochila es mejor que mochila optima
                copia_mochila(mochila_optima, mochila) #Le copio a la mochila optima, la mochila generando una nueva solucion

            optimiza_mochila(mochila, mochila_optima, items, peso_max)

            #Desanotar
            mochila.pop() #Eliminamos los items de la mchila temporalmente
            items.insert(i,objeto) # Inserto el objeto que antes habia quitado



mochila=[] # mochila provisional que vamos generando en cada estado nuevo
mochila_optima=[] # mochila optima
items=[(12,4),(2,2),(1,2),(4,10),(1,1)]
peso_max=15
optimiza_mochila(mochila,mochila_optima,items,peso_max)
print("La mochila vale: "+str(suma_valor(mochila_optima))+" con peso "+str(suma_peso(mochila_optima)))
print(mochila_optima)