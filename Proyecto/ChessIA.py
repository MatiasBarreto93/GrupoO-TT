import random

piecescore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3  # Esta variable controla la profundidad de la IA

knightScores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishopScores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

queenScores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

rookScores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

whitePawnScores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

blackPawnScores =[[0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
                [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]]

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