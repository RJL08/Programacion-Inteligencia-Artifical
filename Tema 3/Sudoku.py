import numpy as np



#Ejercicio Sudoku

def carga(nombre_archivo):
    tablero = [] # lista donde guardamos el tablero
    with open("sudoku.txt", "r") as f: # abrimos el archivo en modo lectura "r"
        for line in f: # leemos cada línea del archivo
            fila = [int(x) for x in line.strip().split(";")] # separamos los numeros por ;
            tablero.append(fila) # añadimos la fila al tablero
    return np.array(tablero)



#2  funcion para  determinar si una fila tiene valores repetidos

def esValidoFila(tablero, fila):
    valores = [x for x in tablero [fila] if x !=0] # ignoramos los ceros
    return len(valores) == len(set(valores)) # comparamos la longitud de la lista con la longitud del conjunto (sin repetidos)

#3 creamos una funcion que determine si una columna tiene valores repetidos

def esValudoColumna(tablero, columna):
    valores = [tablero[i][columna] for i in range(9) if tablero[i][columna] !=0] # ignoramos los ceros
    return len(valores) == len(set(valores))

#4 creamos una funcion que determine si el cuadro de una coordenada del tablero sudoku tiene valores repetidos:

def esValidoCuadro(tablero, fila, columna):
    valores = []
    fila_inicio = (fila // 3) *3
    columna_inicio = (columna // 3)*3

    for i in range(fila_inicio, fila_inicio +3):
        for j in range(columna_inicio, columna_inicio+3):
            if tablero[i][j] !=0:
                valores.append(tablero[i][j])
    return len(valores) == len(set(valores))


#5 creamos un metodo para resolver el sudoku con backtracking




def resolverSudoku(tablero):
    '''
    Resolvemos por medio de backtracking el sudoku
    :param tablero:
    :return:
    '''
    for i in range(9):
        for j in range(9):
            if tablero[i][j] ==0: # encontramos una celda vacia
                for num in range(1,10): # probamos numeros del 1 al 9
                    tablero[i][j] = num # asignamos el numero a la celda
                    if esValidoFila(tablero, i) and esValudoColumna(tablero, j) and esValidoCuadro(tablero, i, j):
                        if resolverSudoku(tablero):
                            return True
                    tablero[i][j] =0 # deshacemos la asignacion
                return False # si no se encuentra un numero vlido, retornamos False
    return True # si se completa el tablero, retornamos True

tablero = carga("sudoku.txt")

print("Sudoku inicial:")
print(tablero)
if resolverSudoku(tablero):
    print(" Sudoku resuelto:")
    print(tablero)
else:
    print(" No se pudo resolver el Sudoku")