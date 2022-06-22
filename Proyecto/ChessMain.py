# Este archivo sera responsable de manejar el input del usuario y mostrar el estado actual del juego (GameState)

import pygame as p
from Proyecto import ChessEngine, ChessIA
import sys
from multiprocessing import Process, Queue

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
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getvalidmoves()
    move_made = False
    loadimages()
    running = True
    square_selected = ()
    player_clicks = []
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = False
    player_two = True

    while running:
        human_turn = (game_state.whiteToMove and player_one) or (not game_state.whiteToMove and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if square_selected == (row, col) or col >= 8:
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2 and human_turn:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makemove(valid_moves[i])
                                move_made = True
                                square_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undomove()
                    move_made = True
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getvalidmoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=ChessIA.findbestmove, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = ChessIA.findRandomMove(valid_moves)
                game_state.makemove(ai_move)
                move_made = True
                ai_thinking = False

        if move_made:
            valid_moves = game_state.getvalidmoves()
            move_made = False
            move_undone = False

        if move_made:
            valid_moves = game_state.getvalidmoves()
            movemade = False
        drawgamestate(screen, game_state, valid_moves, square_selected)
        if game_state.checkmate:
            game_over = True
            if game_state.whiteToMove:
                drawtext(screen, 'Negras Ganan por Jaque-Mate')
            else:
                drawtext(screen, 'Blancas Ganan por Jaque-Mate')
        elif game_state.stalemate:
            game_over = True
            drawtext(screen, 'Tablas')

        clock.tick(MAX_FPS)
        p.display.flip()


# Ilumina los movimientos posibles de la pieza seleccionada

def highlightsquare(screen, gs, validmoves, sqselected):
    if sqselected != ():
        r, c = sqselected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # Ilumina el cuadrado
            s = p.Surface((SQ_SIZE, SQ_SIZE))  # Tamanio
            s.set_alpha(100)  # Trasparencia
            s.fill(p.Color('blue'))  # Color
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))  # Rellena en pantalla
            # Ilumina los movimientos legales
            s.fill(p.Color('yellow'))
            for move in validmoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


# Responsable de todos los graficos del estado actual del juego

def drawgamestate(screen, gs, validmoves, sqselected):
    drawboard(screen)  # Dibuja los cuadrados en la pantalla
    highlightsquare(screen, gs, validmoves, sqselected)  # Dibuja la iluminacion de la pieza seleccionada y movimiento
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


def drawtext(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textobject = font.render(text, True, p.Color('Black'))
    textlocation = p.Rect(0, 0, WIDTH, HEIGHT)\
        .move(WIDTH / 2 - textobject.get_width() / 2, HEIGHT / 2 - textobject.get_height() / 2)
    screen.blit(textobject, textlocation)
    textobject = font.render(text, True, p.Color('Dark Grey'))
    screen.blit(textobject, textlocation.move(2, 2))


if __name__ == "__main__":
    main()

