import random

piecescore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2  # Esta variable controla la profundidad de la IA


def findbestmove(gs, validmoves):
    global nextmove, counter
    nextmove = None
    counter = 0
    random.shuffle(validmoves)  # Randomiza el primer movimiento para que no sea siempre el mismo
    negamax(gs, validmoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)  # Cuantas iteraciones hace el algoritmo por movimiento
    return nextmove


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
        score = -negamax(gs, nextmoves, depth-1, -beta, -alpha, -turnmultiplier)
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
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += piecescore[square[1]]
            elif square[0] == 'b':
                score -= piecescore[square[1]]
    return score
