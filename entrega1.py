from itertools import combinations
from itertools import zip_longest
import numpy as np #Usamos numpy 2.2.2 

"""Función con la que llenaremos la matriz de transición, la cual tendrá como número de filas, el tamaño del alfabeto, y el index i de esta será el 
estado q en una tabla de transicion, es decir, este no estará almacenado textualmente en la matriz.
Esta recibirá:
    n -> cantidad de estados, y por ende, la cantidad de filas de TransitionMatriz
    f -> objeto tipo fichero.
Y retornará la matriz, la cual tendrá la forma:
a | b
  | 
  |   , y el estado q será el index, pues siempre el primer estado será 0."""
def llenarMatriz(n,f):
    matriz=[] #declaramos como lista, pero al agregarle tuplas, se "convierte" en matriz
    i=0
    while(i<n):
        fila=input(f"\tIngrese fila n°{i} de la función de transición: ") #Pedimos datos
        f.write(f"\n\t{i}    {fila}") #Usamos el metodo wirte de objeto fichero para escribir en uno.
        matriz.append(fila.split()) #Añadimos a la matriz cada elemento obtenido en input, al que dividimos por espacios para llenar la matriz.
        i+=1
    f.close() #Cerramos fichero para guardar cambios (hacer flush)
    return matriz #Retornamos matriz de transición

"""Esta función lo que hará es obtener las posibles tuplas al combinar los estados del FDA, haciendo uso de función combinations de Itertools.
Recibe los parámetros: 
    n -> cantidad de estados del DFA
Retorna:
    combinedStates -> lista de los estados combinados."""
def obtenerCombination(n):
    stateList= list(range(n)) #Obtenemos la lista de estados con range de 0 a n-1.
    combinedStates = list(combinations(stateList,2)) #Obtenemos las combinaciones posibles de los estados, y las convertimos a lista.
    return combinedStates

"""Esta función lo que hace es marcar los estados de unmarked (que contiene todas las combinaciones) en los que uno de ellos pertenece al conjunto 
de estados finales Y el otro no, guardandolos en una lista llamada marked, de modo que una vez recorrido unmarked, los elementos de marked sean eliminados de esta,
dejando en unmarked solo los que no hayan sido marcados en este proceso
Parametros: 
    combination -> lista generada con la función obtenerCombinacion y que contiene las posibles combinaciones de los n estados del DFA
    finalStates -> lista que contiene los estados finales
Retorna: una lista con las listas markedStates y unmarkedStates"""
def eliminarMarcados(combination, finalStates):
    markedStates = []  # creamos lista a la que añadiremos los estado marcados

    for (p, q) in combination: #Obtenemos cada tupla en la lista combination
        if ((str(p) in finalStates and str(q) not in finalStates)) or ((str(p) not in finalStates and str(q) in finalStates)): #Verificamos condición de que uno de la tupla pertenezca a finalStates y el otro no
            markedStates.append((p, q))  #añadimos a la lista los que deben marcarse porque cumplen la condicion

    # salimos del for, así que ya terminamos de recorrer unmarked, por lo que ya podemos eliminar los markedStates de unmarkedStates
    unmarkedStates = [pair for pair in combination if pair not in markedStates] #Obtenemos cada par/tupla de combination, y si esa tupla no está en marked, la añadimos a la lista, si no, no.

    return unmarkedStates, markedStates  #por ahora retornamos ambos, en el main dividimos para siguiente funcion tomar solo unmarkedStates


"""Con esta función lo que haremos será reducir los estados equivalentes, es decir, los que tienen la misma transición bajo el mismo símbolo del alfabeto.
iniciara a  recorrer los estados no marcados, y para cada uno de estos, obtendremos los estados a los que puede ir bajo cada símbolo, los agruparemos en tuplas, 
para saacar los esatdos equivalentes (tienen la misma transición bajo el mismo símbolo del alfabeto), y los marcaremos, eliminando los que no lo sean.
Retorna: unmarkedStates -> lista de los estados equivalentes que quedan después de la reducción."""

def reducirEstados(unmarkedStates, markedStates, alphabet, transitionMatrix):
    """Con esta función obtendremos los diferentes estados a los que pueden ir p y q, en (p,q) (tupla de estados) bajo sus respectivos alfabetos.
    Parametros:
        pair -> tupla de estados
        alfabeto -> alfabeto del DFA
        transitionMatrix -> Matriz con tabla de transicion del DFA
        Retorna: nextState -> lista con el conjunto de tuplas que contienen los diferentes estados a los que podemos ir desde p o q, bajo su
        alfabeto, es decir, es la unión de los posibles estados de cada una"""
    def getNextState(pair, alphabet, transitionMatrix):  # Función anidada nos ayuda a conseguir los estados siguientes de una pareja
        """Retorna los siguientes estados de una pareja bajo cada símbolo del alfabeto."""
        nextStates = []
        for i in range(len(alphabet)):  # Para cada símbolo en el alfabeto (a y/o b) obtenemos los estados siguientes
            nextPair = (int(transitionMatrix[pair[0], i]), int(transitionMatrix[pair[1], i])) 
            nextStates.append(tuple(sorted(nextPair)))  # Ordenamos para evitar duplicados y añadimos a la lista
        return nextStates # Retornamos los estados siguientes

    # Lo hacemos n veces hasta que no haya cambios
    prev_size = -1
    while prev_size != len(markedStates): 
        prev_size = len(markedStates)  # Guardamos cuántos estados están marcados antes del ciclo
        marked_for_removal = []  # Lista para los pares que deben marcarse en esta iteración

        for pair in unmarkedStates:
            nextStates = getNextState(pair, alphabet, transitionMatrix)
            if any(state in markedStates for state in nextStates):   # Si alguna transición lleva a un estado marcado, marcamos el par actual
                marked_for_removal.append(pair)

        for pair in marked_for_removal:  # Lo que hacemos es que eliminamos los estados marcados y los agregamos a markedStates
            unmarkedStates.remove(pair)
            markedStates.append(pair)

    return unmarkedStates  #retornamos los estados equivalentes que quedan despues de la reducción


"""Funcion main, donde solicitaremos la mayoria de información y llamaremos a las funciones."""
def main():
    casesNumber= int(input("Ingrese cantidad de casos: "))
    i=0
    f=open("dfa.txt","a") #Abrimos fichero dfa en modo append, para que no se sobreescriban los datos
    f.write(f"\nNúmero de casos: {casesNumber}")
    global alphabet
    while(i<casesNumber):
        #OBTENEMOS DATOS
        f = open("dfa.txt", "a")
        f.write("\n------------------")
        statesNumber=int(input("Número de estados: ")) #int
        alphabet=input("En una sola línea, ingrese el alfabeto separado por un espacio: ").split() #lista al hacer split
        finalStates = input("Ingrese el conjunto de estados finales, separados por un espacio: ").split() #lista

        #ESCRIBIMOS DATO EN TXT
        f.write(f"\nNumero de estados: {statesNumber}")
        f.write(f"\nAlfabeto: {alphabet}")
        f.write(f"\nEstados finales: {finalStates}")
        f.write(f"\nFuncion de transicion: ")
        transitionMatrix= np.array(llenarMatriz(statesNumber,f))
        #f.close() #No es nececsario cerrar f porque ya viene cerrado desde llenarMatriz()

        #Esto debe ir dentro del ciclo porque en cada caso lo debemos calcular
        combination = obtenerCombination(statesNumber)
        estadosAgrupados = eliminarMarcados(combination, finalStates)
        unmarkedStates = list(estadosAgrupados[0])
        markedStates = list(estadosAgrupados[1])
        equivalentes = reducirEstados(unmarkedStates, markedStates, alphabet, transitionMatrix)
        print(equivalentes)

        i+=1 #Actualizamos var

if __name__=="__main__":
    main()     
    
