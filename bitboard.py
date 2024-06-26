from Pieces.piece import *
from Pieces.utils import *
import random
import pygame as p

# global vars for loading image
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}



# for the real board
class Board:
    def __init__(self):
        self.Squares = [None] * 64  # Initialize with 64 None values
        self.turn= "White"
        self.white_pieces = []
        self.black_pieces = []
        self.movelog = []
        self.setup()

    def setup(self):
        # White pieces
        self.Squares[0] = Rook(square=0, color="White", name="wR")
        self.Squares[1] = Knight(square=1, color="White", name="wN")
        self.Squares[2] = Bishop(square=2, color="White", name="wB")
        self.Squares[3] = Queen(square=3, color="White", name="wQ")
        self.Squares[4] = King(square=4, color="White", name="wK")
        self.Squares[5] = Bishop(square=5, color="White", name="wB")
        self.Squares[6] = Knight(square=6, color="White", name="wN")
        self.Squares[7] = Rook(square=7, color="White", name="wR")

        for i in range(8):
            self.Squares[8 + i] = Pawn(square=8 + i, color="White", name=f"wp")

        # Empty squares between the pieces
        for i in range(16, 48):
            self.Squares[i] = 0

        for i in range(8):
            self.Squares[48 + i] = Pawn(square=48 + i, color="Black", name=f"bp")

        self.Squares[56] = Rook(square=56, color="Black", name="bR")
        self.Squares[57] = Knight(square=57, color="Black", name="bN")
        self.Squares[58] = Bishop(square=58, color="Black", name="bB")
        self.Squares[59] = Queen(square=59, color="Black", name="bQ")
        self.Squares[60] = King(square=60, color="Black", name="bK")
        self.Squares[61] = Bishop(square=61, color="Black", name="bB")
        self.Squares[62] = Knight(square=62, color="Black", name="bN")
        self.Squares[63] = Rook(square=63, color="Black", name="bR")
        
        self.update_pieces()

    # Print the board to the screen
       


    def getSquares(self):
        return self.Squares
    
    def getSquare(self, r, c):
        return self.Squares[r * DIMENSION + c]
    
    def getWhitePos(self):
        return self.white_pieces
    
    def getBlackPos(self):
        return self.black_pieces
    
    # set the square of the board equal to a value
    def setSquares(self, index, value):
        self.Squares[index] = value

    def current_turn(self):
        return self.turn
    
    # copy constructor
    def copy(self):
        new_board = Board()
        new_board.Squares = self.Squares.copy()
        new_board.turn = self.turn
        new_board.white_pieces = self.white_pieces.copy()
        new_board.black_pieces = self.black_pieces.copy()
        return new_board

    def toggle_turn(self):
        self.turn = "Black" if self.turn == "White" else "White"

    def update_pieces(self):
        self.white_pieces = []
        self.black_pieces = []

        for idx, piece in enumerate(self.Squares):
            if piece != 0:
                if piece.getColor() == "White":
                    self.white_pieces.append(idx)
                else:
                    self.black_pieces.append(idx)

    def printBoard(self):
        for row in range(7, -1, -1):  # Start from row 7 to row 0
            for col in range(8):
                piece = self.Squares[row * 8 + col]
                if piece != 0:
                    print(piece.getName(), end=" ")
                else:
                    print("--", end=" ")
            print("\n")

    def get_all_legal_moves(self, color):
        legal_moves = []
        pieces = self.white_pieces if color == "White" else self.black_pieces
        
        for index in pieces:
            piece = self.Squares[index]
            piece_moves = piece.legal_moves(self)
            for move in piece_moves:
                legal_moves.append((index, move))

        return legal_moves
    
    # make and unmake moves on the board
    def make_move(self, move):
        start_square, end_square = move
        piece = self.Squares[start_square]
        if piece != 0:
            target_piece = self.Squares[end_square]
            if target_piece != 0 and target_piece.color != piece.color:
                target_piece.alive = False  # Set the captured piece to not be alive
            self.Squares[start_square] = 0
            self.Squares[end_square] = piece
            piece.square = end_square
            self.toggle_turn()
            self.update_pieces()

    def unmake_move(self, move):
        start_square, end_square = move
        piece = self.Squares[end_square]
        if piece != 0:
            # Restore the captured piece if there was one
            target_piece = self.Squares[start_square]
            if target_piece != 0 and target_piece.color != piece.color:
                target_piece.alive = True
            self.Squares[end_square] = target_piece
            self.Squares[start_square] = piece
            piece.square = start_square
            self.toggle_turn()

    #code to implement checkmate check
    def find_king(self, color):
        # Find the square of the king of the given color
        for square, piece in enumerate(self.Squares):
            if piece != 0 and piece.color == color and isinstance(piece, King):
                return square
        return None
    
    def is_check(self, color):
        king_square = self.find_king(color)
        # Check if any opponent's piece can capture the king
        opponent_color = "Black" if color == "White" else "White"
        for piece in self.Squares:
            if piece != 0 and piece.color == opponent_color:
                legal_moves = piece.legal_moves(self)
                if king_square in legal_moves:
                    return True

        return False
    
    def is_checkmate(self, color):
        king_square = self.find_king(color)

        # Check if the king has any legal moves to escape check
        king = self.Squares[king_square]
        king_moves = king.legal_moves(self)
        for move in king_moves:
            board_copy = self.copy()  # Make a copy of the board
            board_copy.make_move((king_square, move))  # Make the move on the copy
            if not board_copy.is_check(color):  # If the king is not in check after the move
                return False  # Not in checkmate

        # Check if any of the king's own pieces can block the check
        opponent_color = "Black" if color == "White" else "White"
        for piece in self.Squares:
            if piece != 0 and piece.color == color:
                legal_moves = piece.legal_moves(self)
                for move in legal_moves:
                    board_copy = self.copy()  # Make a copy of the board
                    board_copy.make_move((piece.getSquare(), move))  # Make the move on the copy
                    if not board_copy.is_check(color):  # If the king is not in check after the move
                        return False  # Not in checkmate

        # If the king has no legal moves and no blocking moves, it's checkmate
        return True
    
    @staticmethod
    def random_move(legal_moves):
        return random.choice(legal_moves)
    
    def play_game(self):
        while True:
            self.printBoard()

            # Check if the current player is in checkmate
            if self.is_checkmate(self.turn):
                print(f"{self.turn} is in checkmate. Game over.")
                break

            # Check if the current player is in check
            if self.is_check(self.turn):
                print(f"{self.turn} is in check.")

            if self.turn == "White":
                # Human player's turn
                print("Your move (e.g., 'e2 e4'): ")
                move_str = input()
                move = (square_to_index(move_str[:2]), square_to_index(move_str[3:]))
                if move in self.get_all_legal_moves("White"):
                    self.make_move(move)
                else:
                    print("Illegal move. Try again.")
                    continue
            else:
                # Bot's turn (random move)
                legal_moves = self.get_all_legal_moves("Black")
                move = Board.random_move(legal_moves)
                print(f"Bot plays: {square_to_chess_notation(move[0])} to {square_to_chess_notation(move[1])}")
                self.make_move(move)
                

# functions for drawing the board
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ' ]
    for pie in pieces:
        IMAGES[pie] = p.transform.scale(p.image.load('C:\\Users\\zane5\\GitHubEngine\\ChessEngine\\images\\' + pie + '.png'), (SQ_SIZE, SQ_SIZE))
        
def drawGameState(screen, board):
    drawBoard(screen)

    drawPieces(screen, board)

def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece =  board.getSquare(r, c)
            if piece != 0:
                screen.blit(IMAGES[piece.getName()], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    

def main():
    # set up board
    board = Board()
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    load_images()

    running = True
    sqSelected = None # Keep track of the last square selected
    playerClicks = [] # Keeps track of the selected square and the target square as two ints i.e [8, 16]

    while running:
        drawGameState(screen, board)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                row = location[0] // SQ_SIZE
                col = location[1] // SQ_SIZE

                idxSelected = row * 8 + col

                if sqSelected == idxSelected:
                    sqSelected == None # if user clicks the same square twice deselect it 
                    playerClicks = []
                else:
                    sqSelected = idxSelected
                    playerClicks.append(sqSelected)

            
                

        clock.tick(MAX_FPS)
        p.display.flip()



        
        
if __name__ == "__main__":
    main()
