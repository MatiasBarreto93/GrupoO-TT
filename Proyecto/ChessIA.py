import random


def findrandommove(validmoves):  # Movimientos legales aleatorios
    return validmoves[random.randint(0, len(validmoves) - 1)]


def findbestmove():
    pass