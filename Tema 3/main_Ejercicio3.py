from grafo_Actividad3 import dibujar_Grafo,vecinos_de,estan_conectados,nodos,aristas



def main():
    print("=== Información del grafo ===")

    # (a) Dibujar grafo
    dibujar_Grafo()

    # (b) Vecinos del nodo B
    print("1) Vecinos del nodo B:", vecinos_de("B"))

    # (b) Si G y H están conectados
    print("2) ¿G y H están conectados?:", estan_conectados("G", "H"))

    # (b) Si D y E están conectados
    print("3) ¿D y E están conectados?:", estan_conectados("D", "E"))

    # (b) Numero de nodos
    print("4) Número de nodos del grafo:", len(nodos))

    # (b) Lista de nodos
    print("5) Lista de nodos:", list(nodos.keys()))


if __name__ == "__main__":
    main()