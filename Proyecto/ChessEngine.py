# Esta clase es responsable de guardar toda la informacion del estado actual del juego y
# determinar los movimientos legales segun el estado actual del juego y tambien generara un log de movimientos

class GameState:
    def __init__(self):
        # Se crea el tablero inicial con las piezas en su lugar correspondiente
        # El primer caracter representa el color
        # El 2do caracter representa el tipo de pieza (R, N, B, Q, K o P)
        # "--" Representa espacio vacio
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []
