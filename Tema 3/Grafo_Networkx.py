import networkx as nx
import matplotlib.pyplot as plt


'''miGrafo= nx.Graph()

miGrafo.add_node('A', pos=(1, 2))
miGrafo.add_node('B', pos=(2, 3))
miGrafo.add_node('E', pos=(2, 1))
miGrafo.add_node('G', pos=(3, 1))
miGrafo.add_node('F', pos=(3, 3))
miGrafo.add_node('C', pos=(3, 4))
miGrafo.add_node('D', pos=(4, 2))

#añadir aristas

miGrafo.add_edge('A', 'B', length=2)
miGrafo.add_edge('A', 'E', length=1)
miGrafo.add_edge('B', 'E', length=3)
miGrafo.add_edge('E', 'G', length=6)
miGrafo.add_edge('G', 'D', length=4)
miGrafo.add_edge('F', 'D', length=1)
miGrafo.add_edge('F', 'G', length=5)
miGrafo.add_edge('F', 'C', length=2)

#las posiciones son las coordenadas
pos = nx.get_node_attributes(miGrafo,'pos')
#pintamos los pesos
etiquetas = nx.get_edge_attributes(miGrafo,'length')
nx.draw_networkx(miGrafo,pos,with_labels=True)
nx.draw_networkx_edge_labels(miGrafo,pos,edge_labels=etiquetas)
plt.show()'''


# Ejercicio de A*

# a_star_lineal_sin_inf.py
from graph import Node, Graph
import matplotlib.pyplot as plt

# -------- Grafo (coordenadas y aristas del esquema) --------
coords = {
    'S':(1,1),'B':(1,2),'C':(1,4),'D':(2,1),'E':(2,2),'F':(2,3),
    'G':(2,4),'H':(3,1),'I':(3,4),'J':(4,1),'K':(4,2),'T':(4,3),'L':(4,4)
}
edges = [
    ('S','D',5),('S','B',5),('B','E',1),('E','D',2),('E','F',6),('F','G',4),
    ('G','C',1),('G','I',3),('I','L',4),('L','T',3),('D','H',3),('H','J',1),
    ('J','K',6),('K','T',2)
]

# crear grafo
g = Graph([Node(v, coords[v]) for v in coords])
for a,b,w in edges:
    g.add_edge(a,b,w)

# --------------------- A* según pseudocódigo ---------------------
# Inicialización
origen, destino = 'S','T'
start  = g.find_node(origen)
goal   = g.find_node(destino)
INFINITO = 999999   # reemplazo de math.inf

for n in g.nodes:
    n.parent = None
    n.distance_from_start = INFINITO   # g(n)
    n.heuristic_value = INFINITO       # f(n)

start.distance_from_start = 0
# f = g + h
start.heuristic_value = abs(start.x - goal.x) + abs(start.y - goal.y)

ABIERTA = [start]
CERRADA = set()
ruta = []

# Búsqueda
while True:
    if not ABIERTA:
        break  # no hay solución

    # seleccionar nodo con menor heurística
    actual = min(ABIERTA, key=lambda n: n.heuristic_value)

    # si es destino -> reconstruir ruta
    if actual.value == goal.value:
        r = actual
        while r:
            ruta.append(r.value)
            r = r.parent
        ruta.reverse()
        break

    # mover actual a CERRADA
    ABIERTA.remove(actual)
    CERRADA.add(actual.value)

    # expandir hijos
    for hijo, peso in actual.neighbors:
        if hijo.value in CERRADA:
            continue

        g_nuevo = actual.distance_from_start + peso

        # actualizar si mejora el camino
        if g_nuevo < hijo.distance_from_start:
            hijo.parent = actual
            hijo.distance_from_start = g_nuevo
            hijo.heuristic_value = g_nuevo + abs(hijo.x - goal.x) + abs(hijo.y - goal.y)
            if hijo not in ABIERTA:
                ABIERTA.append(hijo)

print("Ruta encontrada:", ruta)
print("Coste total:", g.find_node(destino).distance_from_start)

# ------------------------- Dibujo -------------------------

plt.figure()
trazadas=set()

def rotar(nodo):
    return nodo.y, 5 - nodo.x

for a,b,w in edges:
    na, nb = g.find_node(a), g.find_node(b)
    clave = tuple(sorted((a,b)))
    if clave in trazadas:
        continue
    trazadas.add(clave)
    plt.plot([na.x, nb.x], [na.y, nb.y], 'k--', lw=1)
    xm, ym = (na.x+nb.x)/2, (na.y+nb.y)/2
    plt.text(xm, ym, str(w), fontsize=9, ha='center')

for n in g.nodes:
    plt.plot(n.x, n.y, 'o', ms=10, color='gray', alpha=0.6)
    plt.text(n.x, n.y, n.value, ha='center', va='center', fontsize=11)

# Ruta en verde
for i in range(len(ruta)-1):
    a, b = g.find_node(ruta[i]), g.find_node(ruta[i+1])
    plt.plot([a.x,b.x],[a.y,b.y],'g-',lw=3)
for i, nombre in enumerate(ruta):
    n = g.find_node(nombre)
    plt.plot(n.x, n.y, 'o', ms=11, color='green')
    plt.text(n.x, n.y-0.18, str(i), color='blue', fontsize=16, ha='center', va='center')

plt.title('Ruta al destino (A*)')
plt.xlim(0,5); plt.ylim(0,5)
plt.gca().set_aspect('equal'); plt.grid(True)
plt.show()
