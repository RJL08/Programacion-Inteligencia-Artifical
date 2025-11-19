from graph import Node, Graph
import matplotlib.pyplot as plt

'''# un grafo dirijido, con conexion del nodo B al nodo A con peso 3
#dirigido , no hay conexion de A a B

nodoA = Node('A',(1,2)) # con cordenadas (1,2)
NodoB = Node('B',(2,2),[(nodoA,3)]) # b, conecta con a con coste 3


miGrafo = Graph()
miGrafo.add_node(nodoA)
miGrafo.add_node(NodoB)

print(miGrafo)

print("Estan conectado A y B?? ", miGrafo.are_connected('A','B')) # False
print("Estan conectado B y A?? ", miGrafo.are_connected('B','A')) # True

print("El nodo A es mayor que B?? ", nodoA > NodoB) # False



# segundo ejemplo, grafo con cuatro nodos y algunas aristas

nodos=[Node('A',(1,2)),Node('B',(2,2)),
       Node('C',(3,2)),Node('D',(-2,-2))]

miGrafo2=Graph()
for nodo in nodos:
    miGrafo2.add_node(nodo)

miGrafo2.add_edge('A','B',5)
miGrafo2.add_edge('D','C',8)

print(miGrafo2)
print("Estan conectado A y B?? ", miGrafo2.are_connected('A','B')) # True
print("Estan conectado A y D?? ", miGrafo2.are_connected('A','D'))

# pintar en matplotlib con plot

# Pintar en matplotlib con plot
for nodo in miGrafo2.nodes:# Pintar en matplotlib con plot
    # Accedemos a las coordenadas usando los atributos x e y
    x, y = nodo.x, nodo.y
    plt.plot(x, y, 'o', markersize=16, label=nodo.value)
    plt.text(x, y+0.1, nodo.value, fontsize=12, ha='center')

    for neighboor, weight in nodo.neighbors:
        #
        # usamos .x e .y para los vecinos
        x2, y2 = neighboor.x, neighboor.y
        plt.plot([x, x2], [y, y2], 'k-', lw=weight)

# gráfica configuración
plt.title('Grafo')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.axis('equal')
plt.show()'''

# ejercicio

# grafo_ejercicio_sin_bfs.py


# ------------------------------
# 1) Crear nodos con coordenadas
# ------------------------------
# Misma disposición que la diapositiva
A = Node('A', (1.0, 2.0))
B = Node('B', (2.0, 3.0))
E = Node('E', (2.0, 1.0))
G = Node('G', (3.0, 1.0))
F = Node('F', (3.0, 3.0))
C = Node('C', (3.0, 4.0))
D = Node('D', (4.0, 2.0))

# ------------------------------
# 2) Crear el grafo y añadir nodos
# ------------------------------
miGrafo = Graph()
for n in (A, B, C, D, E, F, G):
    miGrafo.add_node(n)

# ----------------------------------
# 3) Añadir aristas (no dirigidas)
#    Pesos como en la imagen
# ----------------------------------
miGrafo.add_edge('A', 'B', 2)
miGrafo.add_edge('A', 'E', 1)
miGrafo.add_edge('B', 'E', 3)
miGrafo.add_edge('E', 'G', 6)
miGrafo.add_edge('G', 'D', 4)
miGrafo.add_edge('F', 'D', 2)
miGrafo.add_edge('F', 'G', 5)
miGrafo.add_edge('F', 'C', 2)

# ----------------------------------
# 4) "Recorrer" el grafo al estilo
#    de tu ejemplo: listar nodos y
#    sus vecinos con pesos
# ----------------------------------
print("=== Recorrido simple (nodo -> vecinos (peso)) ===")
for nodo in miGrafo.nodes:
    vecinos = [f"{v.value}({w})" for (v, w) in nodo.neighbors]
    print(f"{nodo.value} -> {', '.join(vecinos) if vecinos else 'sin vecinos'}")

print("\nComprobaciones rápidas:")
print("¿A y B conectados? ", miGrafo.are_connected('A', 'B'))
print("¿B y A conectados? ", miGrafo.are_connected('B', 'A'))
print("Número de nodos:   ", len(miGrafo.nodes))

# ----------------------------------
# 5) Pintar en matplotlib (como tu
#    ejemplo, con pesos y grosor)
# ----------------------------------
ya_pintadas = set()  # Para no trazar dos veces cada arista

for nodo in miGrafo.nodes:
    x, y = nodo.x, nodo.y
    plt.plot(x, y, 'o', markersize=16)                 # nodo
    plt.text(x, y + 0.18, nodo.value, ha='center', fontsize=12)

    for vecino, peso in nodo.neighbors:
        par = tuple(sorted((nodo.value, vecino.value)))
        if par in ya_pintadas:
            continue
        ya_pintadas.add(par)

        x2, y2 = vecino.x, vecino.y
        plt.plot([x, x2], [y, y2], 'k-', lw=1 + peso/2)  # grosor ≈ peso

        # mostrar el peso en el medio del segmento
        xm, ym = (x + x2) / 2, (y + y2) / 2
        plt.text(xm, ym, str(peso), fontsize=18, ha='center', va='center')

# Configuración del gráfico
plt.title('Grafo (recorrido simple y dibujo)')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.axis('equal')
plt.tight_layout()
plt.show()

