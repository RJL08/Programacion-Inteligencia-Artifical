import matplotlib.pyplot as plt
from graph import Graph, Node
from a_star import AStar

nodos = {"S": (1, 1),"B": (1, 2),"C": (1, 4),"D": (2, 1),"E": (2, 2),
    "F": (2, 3),"G": (2, 4),"H": (3, 1),"I": (3, 4),"J": (4, 1),
    "K": (4, 2),"T": (4, 3),"L": (4, 4)
}

aristas = [("S", "B", 4),("S", "D", 5),("B", "E", 1),("C", "G", 1),("D", "E", 2),("D", "H", 3),("E", "F", 6),
    ("F", "G", 4),("G", "I", 3),("H", "J", 1),("I", "L", 4),("J", "K", 6),("K", "T", 2),("T", "L", 3)
]


def dibujar_Grafo():
    plt.figure(figsize=(10,10))
    plt.ylim([0,5])
    plt.xlim([0,5])

    for origen, destino,peso in aristas:
        x1,y1 = nodos[origen]
        x2,y2 = nodos[destino]
        plt.plot([x1,x2], [y1,y2], '-k',linewidth=2)

        #punto medio
        mx=(x1+x2)/2
        my=(y1+y2)/2
        plt.text(mx,my,str(peso), color='blue', fontsize=18, ha='center', va='bottom')

    for nombre, (x,y) in nodos.items():
        plt.scatter(x,y ,s=700, color='red', edgecolors='none',linewidths=1, zorder=2)
        plt.text(x, y, nombre, ha="center", va="center", fontsize=18, fontweight="bold")

    plt.axis('off')
    plt.show()

    # funcion para buscar vecinos de un nod
def vecinos_de(nodo):
    vecinos = []
    for origen, destino, peso in aristas:
        if origen == nodo:
            vecinos.append((destino, peso))
        elif destino == nodo:
            vecinos.append((origen, peso))
    return vecinos

# funcion para saber si están conectados

def estan_conectados(nodo1, nodo2):
    for origen, destino, peso in aristas:
        if (origen == nodo1 and destino == nodo2) or (origen == nodo2 and destino == nodo1):
            return True
    return False


