import tetris
import gamelib

TAMANOCELDA = 25
ESPERA_DESCENDER = 8
ALTOTABLERO = 450
ANCHOTABLERO = 225
SUPERFICIE = "X"

def procesarpuntuaciones(ruta):
    puntuaciones = []
    with open(ruta) as file:
        for linea in file:
            linea = linea.rstrip("\n")
            if not linea:
                return puntuaciones
            par = linea.split("=")
            puntuaciones.append((par[0], int(par[1])))

    return puntuaciones
def subirpuntuaciones(ruta,listapunutaciones):
    with open(ruta, "w") as file:
        for tupla in listapunutaciones:
            file.write(f"{tupla[0]}={tupla[1]}\n")

def ordenarseleccionpuntuaciones(listapuntajes):
    for i in range(len(listapuntajes) - 1):
        p = buscarminimo(listapuntajes, i)
        listapuntajes[p], listapuntajes[i] = listapuntajes[i], listapuntajes[p]

    return listapuntajes
def buscarminimo(l, i):
    mini = l[i][1]
    min_p = i
    for j in range(i + 1, len(l)):
        if l[j][1] < mini:
            mini = l[j][1]
            min_p = j
    return min_p


def mostrar_juego(juego):
    pieza, superficie, puntuacion = juego

    for x,y in pieza:
        xcentrada = TAMANOCELDA * x + TAMANOCELDA/2
        ycentrada = TAMANOCELDA * y + TAMANOCELDA/2
        gamelib.draw_text("X",xcentrada , ycentrada)
    for columna in range(len(superficie)):
        for fila in range(len(superficie[0])):
            if superficie[columna][fila] == tetris.SUPERFICIE:
                x = TAMANOCELDA * columna +TAMANOCELDA/2
                y = TAMANOCELDA * fila + TAMANOCELDA/2
                gamelib.draw_text("X",x,y)
    gamelib.draw_text(puntuacion, 325, 300 )
def dibujar_siguiente(piezasig):
    for x,y in piezasig:
        gamelib.draw_text("X", 300 + x*TAMANOCELDA +10, 50 + y*TAMANOCELDA + 10, size=TAMANOCELDA )


def main():

    # Inicializar el estado del juego
    gamelib.resize(400, 450)
    pieza = tetris.generar_pieza()
    juego = tetris.crear_juego(pieza)
    pieza_i = tetris.generar_pieza()
    timer_bajar = ESPERA_DESCENDER
    while gamelib.loop(fps=10):


        gamelib.draw_begin()
        gamelib.draw_text("SIGUIENTE PIEZA: ", 300,20)
        gamelib.draw_text("PUNTAJE:", 275, 300)
           #lineas verticales
        for i in range(1,10):
            gamelib.draw_line(TAMANOCELDA * i, 0, TAMANOCELDA * i, ALTOTABLERO)
        #lineas horizontales
        for i in range(1,tetris.ALTO_JUEGO):
            gamelib.draw_line(0,TAMANOCELDA*i, ANCHOTABLERO, TAMANOCELDA * i)
        # Dibujar la pantalla
        gamelib.draw_end()

        for event in gamelib.get_events():
            if not event:
                break

            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key
                dicteclas = tetris.pasar_a_diccionario("teclas.txt")
                a = dicteclas.get(tecla, None)

                if a == "ROTAR":
                    juego = tetris.rotar(juego)

                if a == "DESCENDER":
                    juego, _ = tetris.avanzar(juego, pieza_i)
                    if  _ :
                        pieza_i = tetris.generar_pieza()
                if a == "IZQUIERDA":
                    juego = tetris.mover(juego, tetris.IZQUIERDA)

                if a == "DERECHA":
                    juego = tetris.mover(juego,tetris.DERECHA)
                if a == "GUARDAR":
                    juego = tetris.guardar_partida(juego,"partida.txt")
                if a == "CARGAR":
                    juego = tetris.cargar_partida("partida.txt")
                if a == "SALIR":
                    return


                # Actualizar el juego, según la tecla presionada

        timer_bajar -= 1
        if timer_bajar == 0:

            juego, _ = tetris.avanzar(juego, pieza_i)
            if _ :
                pieza_i = tetris.generar_pieza()
            timer_bajar = ESPERA_DESCENDER

            # Descender la pieza automáticamente

        if tetris.terminado(juego):
            pieza, superficie, puntuacion = juego
            gamelib.draw_text("PERDISTE", 175, 80, size=40)
            nombre = gamelib.input("ingrese su nombre")
            listapuntuaciones = procesarpuntuaciones("puntuaciones.txt")
            listapuntuaciones.append((nombre, int(puntuacion)))
            lista = ordenarseleccionpuntuaciones(listapuntuaciones)
            lista.reverse()#la damos vuelta porque esta ordenada de menor a mayor y queremos que el archivo empieze leyendo de mayor a menor 


            if len(lista) > 10:
                lista = lista[:10]
                print(lista)
            subirpuntuaciones("puntuaciones.txt", lista)

            break

        mostrar_juego(juego)
        dibujar_siguiente(pieza_i)
gamelib.init(main)


