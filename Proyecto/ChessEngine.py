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
        self.movefunctions = {'P': self.getpawnmoves, 'R': self.getrookmoves, 'N': self.getknightmoves,
                              'B': self.getbishopmoves, 'Q': self.getqueenmoves, 'K': self.getkingmoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whitekinglocation = (7, 4)
        self.blackkinglocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPosible = ()  # Coordenadas o cuadrado donde es posible la captura

    def makemove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # Se agrega el movimiento al log
        self.whiteToMove = not self.whiteToMove
        #  Se actualiza la posicion del rey
        if move.pieceMoved == 'wK':
            self.whitekinglocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackkinglocation = (move.endRow, move.endCol)

        # Promocion Peon
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # Movimiento captura al paso - Passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'  # Captura el peon

        # Actualiza la variable enpassantPossible
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            # Solamente cuando el peon avanza 2 cuadrados
            self.enpassantPosible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPosible = ()

    # Deshace el ultimo movimiento realizado
    def undomove(self):
        if len(self.moveLog) != 0:  # Se asegura de que exista un movimiento para deshacer
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #  Se actualiza la posicion del rey al revertir el movimiento
            if move.pieceMoved == 'wK':
                self.whitekinglocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackkinglocation = (move.startRow, move.startCol)
            # Deshacer movimiento captura al paso - Passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'  # Vacío el cuadrado
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPosible = (move.endRow, move.endCol)
            # Deshacer avance de dos cuadrados del peon
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPosible = ()

    # Todos los movimientos incluyendo jaque
    def getvalidmoves(self):
        tempenpassantpossible = self.enpassantPosible
        # 1) Genera todos los posibles movimientos
        moves = self.getallposiblesmoves()
        # 2) Por cada movimiento hace un movimiento
        for i in range(len(moves) - 1, -1, -1):  # Se remueve de la lista de movimientos de forma inversa
            self.makemove(moves[i])
            # 3) Genera todos los movimientos enemigos posibles
            # 4) Por cada movimiento enemigo, se fija si esta atacando al rey blanco
            self.whiteToMove = not self.whiteToMove
            if self.incheck():
                moves.remove(moves[i])  # 5) Si se sigue atacando el rey no es un movimiento valido
            self.whiteToMove = not self.whiteToMove
            self.undomove()
        if len(moves) == 0:  # Se fija si es jaque o jaque-mate
            if self.incheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.enpassantPosible = tempenpassantpossible
        return moves

    # Determina si el jugador del turno actual esta en jaque
    def incheck(self):
        if self.whiteToMove:
            return self.squareunderattack(self.whitekinglocation[0], self.whitekinglocation[1])
        else:
            return self.squareunderattack(self.blackkinglocation[0], self.blackkinglocation[1])

    # Determina si el enemigo puede atacar al rey en su posicion
    def squareunderattack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # Cambia al punto de vista del enemigo actual
        oppmoves = self.getallposiblesmoves()
        self.whiteToMove = not self.whiteToMove  # Cambia de turno nuevamente
        for move in oppmoves:
            if move.endRow == r and move.endCol == c:  # Identifica si ese cuadrado esta bajo ataque
                return True
        return False

    # Todos los movimientos sin incluir jaque
    def getallposiblesmoves(self):
        # moves = [Move((6, 4), (4, 4), self.board)] Test del algoritmo
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.movefunctions[piece](r, c, moves)  # Llama al diccionario de funciones
        return moves

    # Movimiento de los peones
    def getpawnmoves(self, r, c, moves):
        if self.whiteToMove:  # Turno del jugador blanco
            if self.board[r - 1][c] == "--":  # Movimiento de 1 lugar si esta vacio
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # Movimiento de 2 lugares si es el 1er movimiento y vacio
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # Captura la ficha enemiga que esta a la izquierda
                if self.board[r - 1][c - 1][0] == 'b':  # Verifica si hay una ficha de otro color y la captura
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1, c-1) == self.enpassantPosible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isenpassantmove=True))
            if c + 1 <= 7:  # Captura la ficha enemiga que esta a la derecha
                if self.board[r - 1][c + 1][0] == 'b':  # Verifica si hay una ficha de otro color y la captura
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r-1, c+1) == self.enpassantPosible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isenpassantmove=True))
        else:  # Turno del jugador negro
            if self.board[r + 1][c] == "--":  # Movimiento de 1 lugar si esta vacio
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # Movimiento de 2 lugares si es el 1er movimiento y vacio
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # Captura la ficha enemiga que esta a la izquierda
                if self.board[r + 1][c - 1][0] == 'w':  # Verifica si hay una ficha de otro color y la captura
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1, c-1) == self.enpassantPosible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isenpassantmove=True))
            if c + 1 <= 7:  # Captura la ficha enemiga que esta a la derecha
                if self.board[r + 1][c + 1][0] == 'w':  # Verifica si hay una ficha de otro color y la captura
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1, c+1) == self.enpassantPosible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isenpassantmove=True))

    # Movimiento de las torres
    def getrookmoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Arriba, Izquierda, Abajo y Derecha
        enemycolor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:  # Verifica que se encuentre en el tablero
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--":  # Verifica que el cuadrado este vacio
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                    elif endpiece[0] == enemycolor:  # Verifica que la pieza sea enemiga
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                        break
                    else:  # Detecta que la pieza es aliada
                        break
                else:  # Detecta que se encuentra fuera del tablero
                    break

    # Movimiento de los caballos
    def getknightmoves(self, r, c, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allycolor = "w" if self.whiteToMove else "b"
        for m in directions:
            endrow = r + m[0]
            endcol = c + m[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] != allycolor:  # Espacio vacio o ficha enemiga
                    moves.append(Move((r, c), (endrow, endcol), self.board))

    # Movimiento de los alfiles
    def getbishopmoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # 4 Diagonales
        enemycolor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # Como máximo los alfiles pueden moverse 7
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:  # Verifica que se encuentre en el tablero
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--":  # Verifica que el cuadrado este vacio
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                    elif endpiece[0] == enemycolor:  # Verifica que la pieza sea enemiga
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                        break
                    else:  # Detecta que la pieza es aliada
                        break
                else:  # Detecta que se encuentra fuera del tablero
                    break

    # Movimiento de la reina
    def getqueenmoves(self, r, c, moves):
        self.getrookmoves(r, c, moves)
        self.getbishopmoves(r, c, moves)

    # Movimiento del rey
    def getkingmoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allycolor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endrow = r + directions[i][0]
            endcol = c + directions[i][1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] != allycolor:  # Espacio vacio o ficha enemiga
                    moves.append(Move((r, c), (endrow, endcol), self.board))


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board, isenpassantmove=False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        # Promocion del peor
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or \
                               (self.pieceMoved == 'bP' and self.endRow == 7)
        # Captura al paso - Passant
        self.isEnpassantMove = isenpassantmove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getchessnotation(self):
        return self.getrankfile(self.startRow, self.startCol) + self.getrankfile(self.endRow, self.endCol)

    def getrankfile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
