from graph import Graph, Node
from a_star import AStar

def run():
    # Create graph
    graph = Graph()
    # Add vertices
    graph.add_node(Node('S', (1,1)))
    graph.add_node(Node('B', (1,2)))
    graph.add_node(Node('C', (1,4)))
    graph.add_node(Node('D', (2,1)))
    graph.add_node(Node('E', (2,2)))
    graph.add_node(Node('F', (2,3)))
    graph.add_node(Node('G', (2,4)))
    graph.add_node(Node('H', (3,1)))
    graph.add_node(Node('I', (3,4)))
    graph.add_node(Node('J', (4,1)))
    graph.add_node(Node('K', (4,2)))
    graph.add_node(Node('T', (4,3)))
    graph.add_node(Node('L', (4,4)))
    
    # Add edges
    graph.add_edge('S', 'B', 4)
    graph.add_edge('S', 'D', 5)
    graph.add_edge('B', 'E', 1)
    graph.add_edge('C', 'G', 1)
    graph.add_edge('D', 'E', 2)
    graph.add_edge('D', 'H', 3)
    graph.add_edge('E', 'F', 6)
    graph.add_edge('F', 'G', 4)
    graph.add_edge('G', 'I', 3)
    graph.add_edge('H', 'J', 1)
    graph.add_edge('I', 'L', 4)
    graph.add_edge('J', 'K', 6)
    graph.add_edge('K', 'T', 2)
    graph.add_edge('T', 'L', 3)

    # Execute the algorithm
    alg = AStar(graph, "S", "T")
    path, path_length = alg.search()
    print(" -> ".join(path))
    print(f"Length of the path: {path_length}")
    
    import matplotlib.pyplot as plt
    
    plt.title("Ruta al destino")
    plt.ylim([0,5])
    plt.xlim([0,5])
    x=[]
    y=[]
    
    colores=[]
    for i in graph.nodes:
        x.append(i.x)
        y.append(i.y)
        
        plt.annotate(i.value, (i.x,i.y),xytext=(i.x+0.1,i.y+0.2))
        colores.append("green" if i.value in path else "#a0a0a0")
        vecinosx=[]
        vecinosy=[]
        for j in i.neighbors:    
            vecinosx.extend([j[0].x,i.x])
            vecinosy.extend([j[0].y,i.y])
        plt.plot(vecinosx,vecinosy,"*-k")
        
    caminox=[]
    caminoy=[]
    for indice,i in enumerate(path):
        nodo=graph.find_node(i)
        caminox.append(nodo.x)
        caminoy.append(nodo.y)
        plt.annotate(indice,(nodo.x,nodo.y),c="blue",xytext=(nodo.x+0.1,nodo.y-0.3),fontsize=8)
        
        
        
    plt.scatter(x=x,y=y,c=colores,s=100)
    plt.plot(caminox,caminoy,"*--",color="#66ff66")
    
    
    
    plt.show()
    

if __name__ == '__main__':
  run()

# S -> D -> H -> J -> K -> T
# Length of the path: 17

