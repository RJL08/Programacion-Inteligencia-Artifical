from graph import Node, Graph
import networkx as nx
import matplotlib.pyplot as plt


grafo = nx.Graph()

#añadimos los anodos

grafo.add_nodes_from(list("ABCDEFGH"))

#añadimos las aristas con los pesos

edge = [("A","B",5),("A","C",2),("B","D",2),("C","D",7),("B","E",4),
        ("D","E",1),("E","F",15),("E","G",12),("F","G",1)]

grafo.add_weighted_edges_from(edge)

# posiciones
pos = {"A": (0.0, 0.55),"B": (1.0, 1.15),"C": (1.0, 0.00),"D": (2.05, 0.00),
    "E": (3.05, 0.80),"F": (4.05, 0.00),"G": (4.65, 1.15),"H": (5.30, 0.80),  # nodo aislado a la derecha
        }

plt.figure(figsize=(10,3))

#dibujamos los nodos
nx.draw(grafo, pos, node_color='red', edge_color='white',node_size=900,with_labels=True)
#dibujamos las aristas
nx.draw_networkx_edges(grafo, pos, width=2)
#dibujamos las etiquetas de las aristas
etiquetas = nx.get_edge_attributes(grafo,'weight')
nx.draw_networkx_edge_labels(grafo,pos,edge_labels=etiquetas)
plt.title("Grafo con NetworkX")
plt.axis('off')
plt.show()
