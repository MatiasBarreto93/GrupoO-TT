# Este archivo sera responsable de manejar el input del usuario y mostrar el estado actual del juego (GameState)

import pygame as p
from Proyecto import ChessEngine

WIDTH = HEIGHT = 512  # Dimensiones
DIMENSION = 8  # Se divide en 8 col y 8 fil
SQ_SIZE = HEIGHT // DIMENSION  # Tamaño de los cuadrados
MAX_FPS = 15  # Para animaciones
IMAGES = {}


# Se crea un diccionario de images, el cual sera llamado en el main y se cargara una vez para optimizar el programa

def loadimages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# Esta parte se encarga de manejar el input del usuario y de actualizar los graficos

def main():
    p.init()
    screen = p.display.set_mode(size=(WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validmoves = gs.getvalidmoves()
    movemade = False  # Variable que indica cuando se realiza un movimiento
    loadimages()
    running = True
    sqselected = ()
    playerclicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Controles mouse
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # Coordenadas (x,y) posicion del mouse
                col = location[0] // SQ_SIZE  # Detecta el click en el cuadrado
                row = location[1] // SQ_SIZE
                if sqselected == (row, col):
                    sqselected = ()
                    playerclicks = []
                else:
                    sqselected = (row, col)
                    playerclicks.append(sqselected)
                if len(playerclicks) == 2:
                    move = ChessEngine.Move(playerclicks[0], playerclicks[1], gs.board)
                    print(move.getchessnotation())
                    for i in range(len(validmoves)):
                        if move == validmoves[i]:
                            gs.makemove(validmoves[i])
                            movemade = True
                            sqselected = ()  # Resetea los clicks del usuario
                            playerclicks = []
                    if not movemade:
                        playerclicks = [sqselected]
            # Controles teclas
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Deshace movimiento realizado cuando se presiona la tecla 'z'
                    gs.undomove()
                    movemade = True
        if movemade:
            validmoves = gs.getvalidmoves()
            movemade = False

        drawgamestate(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


# Responsable de todos los graficos del estado actual del juego

def drawgamestate(screen, gs):
    drawboard(screen)  # Dibuja los cuadrados en la pantalla
    drawpieces(screen, gs.board)  # Dibuja las piezas segun el estado actual


def drawboard(screen):
    colors = [p.Color(255, 241, 221), p.Color(181, 148, 109)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawpieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]  # Es posible combiar las funciones drawBoard y drawPieces en la misma funcion,
            if piece != "--":  # pero de esta forma es mas facil debuggear
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
