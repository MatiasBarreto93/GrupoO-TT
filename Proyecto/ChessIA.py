import random

piecescore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2  # Esta variable controla la profundidad de la IA

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 4, 3, 3, 3, 3, 4, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

piecePositionScores = {"N": knightScores, "Q": queenScores, "B": bishopScores, "R": rookScores,
                       "bP": blackPawnScores, "wP": whitePawnScores}


def findbestmove(gs, validmoves, return_queue):
    global nextmove, counter
    nextmove = None
    counter = 0
    random.shuffle(validmoves)  # Randomiza el primer movimiento para que no sea siempre el mismo
    negamax(gs, validmoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)  # Cuantas iteraciones hace el algoritmo por movimiento
    return return_queue.put(nextmove)


def negamax(gs, validmoves, depth, alpha, beta, turnmultiplier):
    global nextmove, counter
    counter += 1
    if depth == 0:
        return turnmultiplier * scoreboard(gs)  # Seleccion del turno
    maxscore = -CHECKMATE
    for move in validmoves:
        gs.makemove(move)
        nextmoves = gs.getvalidmoves()
        # Se llama recursivamente hasta alcanzar una profundidad de 0
        score = -negamax(gs, nextmoves, depth - 1, -beta, -alpha, -turnmultiplier)
        if score > maxscore:
            maxscore = score
            if depth == DEPTH:  # Si la profundidad esta en el nivel maximo
                nextmove = move
        gs.undomove()
        # Pruning
        if maxscore > alpha:  # Aca sucede el cambio y solo revisa las ramas con menor score
            alpha = maxscore
        if alpha >= beta:  # Si encuentra la mejor rama , descarta el resto y sale del bucle
            break
    return maxscore


def scoreboard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # Negras ganan
        else:
            return CHECKMATE  # Blancas ganan
    elif gs.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":  # Comprobamos que no sea un espacio en blanco
                # Calificamos posicionalmente
                piecepositionscore = 0
                if square[1] != "K":  # Si en el cuadrado no hay un rey
                    if square[1] == "P":  # Si en el cuadrado hay un peon
                        piecepositionscore = piecePositionScores[square][row][col]
                    else:  # Si en el cuadrado hay otra pieza
                        piecepositionscore = piecePositionScores[square[1]][row][col]
                if square[0] == 'w':
                    score += piecescore[square[1]] + piecepositionscore * 0.1
                elif square[0] == 'b':
                    score -= piecescore[square[1]] + piecepositionscore * 0.1
    return score


def findRandomMove(valid_moves):
    return random.choice(valid_moves)
