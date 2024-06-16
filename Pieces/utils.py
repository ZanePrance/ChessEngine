from Pieces.piece import *
from bitboard import Board
import random

def square_to_chess_notation(square):
    if not (0 <= square <= 63):
        raise ValueError("Square must be between 0 and 63")

    file = square % 8
    rank = square // 8

    file_letter = chr(ord('A') + file)
    rank_number = rank + 1

    return f"{file_letter}{rank_number}"

def square_to_index(square_notation):
    file = square_notation[0]
    rank = square_notation[1]
    
    fileNum = 0
    rankNum = 0
    #get file num
    if file == "a":
        fileNum = 0
    elif file == "b":
        fileNum = 1
    elif file == "c":
        fileNum = 2
    elif file == "d":
        fileNum = 3
    elif file == "e":
        fileNum = 4
    elif file == "f":
        fileNum = 5
    elif file == "g":
        fileNum = 6
    elif file == "h":
        fileNum = 7

    # get rank value
    if rank == "1":
        rankNum = 0
    elif rank == "2":
        rankNum = 1
    elif rank == "3":
        rankNum = 2
    elif  rank == "4":
        rankNum = 3
    elif  rank == "5":
        rankNum = 4
    elif  rank == "6":
        rankNum = 5
    elif  rank == "7":
        rankNum = 6
    elif  rank == "8":
        rankNum = 7
    
    return rankNum * 8 + fileNum


