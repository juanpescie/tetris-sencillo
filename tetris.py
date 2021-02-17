ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6
import csv
import random
VACIO = "v"
SUPERFICIE = "s"
puntuaciones = []


def constpiezas(archivo):
    piezas = []
    with open(archivo) as file:
        for linea in file:
            rotaciones = []
            i = linea.find("#")
            linea= linea.rstrip("\n")[:i-1]
            listatuplas = linea.split()
            for i in range(len(listatuplas)):
                rotacion = []
                pares = listatuplas[i].split(";")
                for i in range(len(pares)):
                    coordenadas = pares[i].split(",")
                    x = int(coordenadas[0])
                    y = int(coordenadas[1])
                    rotacion.append((x,y))
                rotaciones.append(tuple(rotacion))

            piezas.append(tuple(rotaciones))

    return tuple(piezas)
PIEZAS = constpiezas("piezas.txt")

def generar_pieza(pieza=None, rotacion=0):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    pieza_azar = random.choice(PIEZAS)
    if pieza == None:
        return pieza_azar[rotacion]
    else:
        return PIEZAS[pieza][rotacion]
def encontrarindices(pieza_a_rotar,piezas):
    for i in range(len(piezas)):
        if pieza_a_rotar in piezas[i]:
            indice = i
            subindrotacion = piezas[i].index(pieza_a_rotar) % len(piezas[i])
            return indice, subindrotacion
def buscar_rotacion(pieza, rotaciones):
    i,j = encontrarindices(pieza, rotaciones)
    return PIEZAS[i][(j+1) % len(rotaciones[i])]

def ordenar_por_coordenadas(pieza_a_rotar):
    c = sorted(pieza_a_rotar)
    return c
def rotar(juego):
    pieza, superficie, puntuacion = juego
    pieza_ordenada = ordenar_por_coordenadas(pieza)
    primer_posicion = pieza_ordenada[0]
    pieza_en_origen = trasladar_pieza(pieza_ordenada, -primer_posicion[0], -primer_posicion[1])
    siguiente_rotacion = buscar_rotacion(pieza_en_origen, PIEZAS)
    trasladada = trasladar_pieza(siguiente_rotacion, primer_posicion[0], primer_posicion[1])
    for x,y in trasladada:
        if x < 0 or x >= ANCHO_JUEGO or y < 0 or y >= ALTO_JUEGO or superficie[x][y] == SUPERFICIE:
            return juego
    juego = trasladada,superficie, puntuacion
    return juego

def trasladar_pieza(pieza,dx, dy ):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """

    nueva = []
    for x,y in pieza:
        suma_diferenciales = (x + dx, y + dy)
        nueva.append(suma_diferenciales)
    return tuple(nueva)

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    pieza_centrada= trasladar_pieza(pieza_inicial, ANCHO_JUEGO//2 ,0)

    superficie = []
    for columna in range(ANCHO_JUEGO):
        superficie.append([])
        for fila in range(ALTO_JUEGO):
            superficie[columna].append(VACIO)
#ponemos una v para representar el vacio
#y en caso de que haya superficie ponemos una s

    puntuacion = 0

    juego = pieza_centrada,superficie, puntuacion

    return juego

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    pieza, superficie, puntuacion = juego

    return pieza

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    pieza,superficie, puntuacion = juego
    ancho = len(superficie)
    alto = len(superficie[0])

    return (ancho,alto)
def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    pieza_centrada, superficie, puntuacion = juego
    if superficie[x][y] == SUPERFICIE:
        return True
    return False


def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    pieza, superficie, puntuacion = juego

    desplazada = trasladar_pieza(pieza, direccion, 0)

    for x,y in desplazada:
        if x < 0 or x >= ANCHO_JUEGO or superficie[x][y] == SUPERFICIE:
            return juego

    juego_desplazado = desplazada, superficie, puntuacion

    return juego_desplazado
def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar incorporar la nueva pieza arriba
    de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    pieza, superficie, puntuacion = juego

    pieza_baja = trasladar_pieza(pieza_actual(juego) ,0,1)
    juego_alte = pieza_baja, superficie, puntuacion
    pieza_nueva = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)

    cambiar_pieza = False

    if terminado(juego):
        return (juego,cambiar_pieza)

    for x,y in pieza_baja:
        if y == ALTO_JUEGO or hay_superficie(juego_alte,x,y) :
            superficie = consolidar_pieza(juego)
            cambiar_pieza= True
            pieza = pieza_nueva
            puntuacion += len(pieza)

            break

        else:
            pieza = pieza_baja

    superficie_limpia = eliminar_filas_llenas(superficie)

    juego_nuevo = pieza, superficie_limpia, puntuacion


    return (juego_nuevo, cambiar_pieza)

def eliminar_filas_llenas(superficie):
    for f in range(len(superficie[0])):
        if all(superficie[c][f] == SUPERFICIE for c in range(len(superficie))):
            for c in range(len(superficie)):
                superficie[c].pop(f)
                superficie[c].insert(0, VACIO)
    return superficie

def consolidar_pieza(juego):
    pieza, superficie, puntuacion = juego

    for x,y in pieza:
        superficie[x][y] = SUPERFICIE

    return superficie
def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    pieza = pieza_actual(juego)
    for x,y in pieza:
        if y == 0 :
            for x,y in pieza:
                if hay_superficie(juego,x,y):
                    return True
        return False
def guardar_partida(juego, ruta):
    pieza, superficie, puntuacion = juego
    strpieza = ""
    for x,y in pieza:
        strpieza += f"{x},{y}|"
    strpieza = strpieza.rstrip("|")
    strsuperficie = ""
    for c in range(len(superficie)):
        for f in range(len(superficie[0])):
            strsuperficie += f"{superficie[c][f]},"
        strsuperficie= strsuperficie.rstrip(",")
        strsuperficie += "|"
    strsuperficie = strsuperficie.rstrip("|")

    with open(ruta,"w") as file:
        file.write(strpieza + "\n")
        file.write(strsuperficie + "\n")
        file.write(str(puntuacion))
    return juego

def cargar_partida(ruta):

    with open(ruta) as file:
        piezaformada = []
        superficiefinal = []
        pieza = file.readline()
        pares = pieza.rstrip("\n").split("|")
        for par in pares:
            par = par.split(",")
            piezaformada.append((int(par[0]), int(par[1])))

        superficie = file.readline()
        superficies = superficie.rstrip("\n").split("|")
        for conjunto in superficies:
            unasola = conjunto.split(",")
            superficiefinal.append(unasola)
        puntuacionstr = file.readline().rstrip()
        puntuacion = int(puntuacionstr)
    juego = tuple(piezaformada), superficiefinal, puntuacion
    return juego


def pasar_a_diccionario(ruta):
    nuevodic = {}
    with open(ruta) as file:
        linea = csv.reader(file, delimiter="=")
        for clave,valor in linea:
            nuevodic[clave] = valor
    return nuevodic




