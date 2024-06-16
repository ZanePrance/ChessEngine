
#Parent class of all pieces
class Piece:
    def __init__(self, square, value, color, name, alive=True):
        self.square = square
        self.value = value
        self.color = color
        self.alive = alive
        self.name = name

    def move(self):
        raise NotImplementedError("This method should be overridden by subclass")
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.color}, {'Alive' if self.alive else 'Captured'})"
    
    #getters
    def getName(self):
        return self.name
    
    def getColor(self):
        return self.color
    
    def getValue(self):
        return self.value
    
    def getSquare(self):
        return self.square
    
    def isAlive(self):
        return self.alive
    
    def legal_moves(self, board):
        possible_moves = self.move()
        legal_moves = []

        for move in possible_moves:
            target_piece = board.getSquares()[move]
            if target_piece == 0:
                legal_moves.append(move)
            elif target_piece.color != self.color:
                legal_moves.append(move)
                break
            else:
                break

        return legal_moves
    
    
    
  
#derived classes
class Pawn(Piece):
    def __init__(self, square, color, name):
        super().__init__(square, value=1, color=color, name=name)
        self.first_move = True
    
    def move(self):
        possible_moves = []
        row = self.square // 8
        col = self.square % 8
        direction = 1 if self.color == "White" else -1

        # Forward moves
        one_step = self.square + direction * 8
        if 0 <= one_step < 64:
            possible_moves.append(one_step)

        if self.first_move:
            two_step = self.square + direction * 16
            if 0 <= two_step < 64:
                possible_moves.append(two_step)


        # Diagonal captures
        capture_moves = [
            (row + direction, col + 1),
            (row + direction, col - 1)
        ]

        for r, c in capture_moves:
            if 0 <= r < 8 and 0 <= c < 8:
                possible_moves.append(r * 8 + c)

        return possible_moves
    
    def legal_moves(self, board):
        possible_moves = self.move()
        legal_moves = []
        direction = 1 if self.color == "White" else -1
        for move in possible_moves:
            target_piece = board.getSquares()[move]
            if move == self.square + direction * 8:
                if target_piece == 0:
                    legal_moves.append(move)
            elif move == self.square + direction * 16:
                if self.first_move and target_piece == 0 and board.getSquares()[self.square + direction * 8] == 0:
                    legal_moves.append(move)
            elif abs(move - self.square) in [7, 9]:
                if target_piece != 0 and target_piece.color != self.color:
                    legal_moves.append(move)

        return legal_moves

    def move_piece(self, destination, board):
        board.setSquares(self.square, 0)
        self.square = destination
        board.setSquares(destination, self)
        self.first_move = False
    
class Rook(Piece):
    def __init__(self, square, color, name):
        super().__init__(square, value=5, color=color, name=name)
    
    def move(self):
        possible_moves = []
        row = self.square // 8
        col = self.square % 8

        # Moves in the same row
        for c in range(8):
            if c != col:
                possible_moves.append(row * 8 + c)

        # Moves in the same column
        for r in range(8):
            if r != row:
                possible_moves.append(r * 8 + col)

        return possible_moves
    

class Bishop(Piece):
    def __init__(self, square, color, name):
        super().__init__(square, value=3, color=color, name=name)
    
    def move(self):
        possible_moves = []
        row = self.square // 8
        col = self.square % 8

        # Diagonal moves (top-right, top-left, bottom-right, bottom-left)
        directions = [
            (1, 1),   # Top-right
            (1, -1),  # Top-left
            (-1, 1),  # Bottom-right
            (-1, -1)  # Bottom-left
        ]

        for direction in directions:
            r, c = row, col
            while True:
                r += direction[0]
                c += direction[1]
                if 0 <= r < 8 and 0 <= c < 8:
                    possible_moves.append(r * 8 + c)
                else:
                    break

        return possible_moves

class Knight(Piece):
    def __init__(self, square, color, name):
        super().__init__(square, value=3, color=color, name=name)
    
    def move(self):
        possible_moves = []
        row = self.square // 8
        col = self.square % 8

        directions = [
            (1, 2), # Up 1 over right 2
            (1, -2), # Up 1 over left 2
            (2, 1), # Up 2 over right 1
            (2, -1), # Up 2 over left 1
            (-1, 2), # Down 1 over right 2
            (-1, -2), # Down 1 over left 2
            (-2, 1), # Down 2 over right 1
            (-2, -1) # Down 2 over left 1
        ]
        for direction in directions:
            r, c = row + direction[0], col + direction[1]
            if 0 <= r < 8 and 0 <= c < 8:
                possible_moves.append(r * 8 + c)

        return possible_moves

    def legal_moves(self, board):
        possible_moves = self.move()
        legal_moves = []

        for move in possible_moves:
            target_piece = board.getSquares()[move]
            if target_piece == 0 or target_piece.color != self.color:
                legal_moves.append(move)

        return legal_moves



class Queen(Piece):
    def __init__(self, square, color, name):
        super().__init__(square, value=9, color=color, name=name)
    
    def move(self):
        possible_moves = []
        row = self.square // 8
        col = self.square % 8

        # Diagonal moves (top-right, top-left, bottom-right, bottom-left)
        directions = [
            (1, 1),   # Top-right
            (1, -1),  # Top-left
            (-1, 1),  # Bottom-right
            (-1, -1)  # Bottom-left
        ]

        for direction in directions:
            r, c = row, col
            while True:
                r += direction[0]
                c += direction[1]
                if 0 <= r < 8 and 0 <= c < 8:
                    possible_moves.append(r * 8 + c)
                else:
                    break
        # Moves in the same row
        for c in range(8):
            if c != col:
                possible_moves.append(row * 8 + c)

        # Moves in the same column
        for r in range(8):
            if r != row:
                possible_moves.append(r * 8 + col)

        return possible_moves

# debug the king moves
class King(Piece):
    def __init__(self, square, color, name):
        super().__init__(square, value=1000, color=color, name=name)
    
    def move(self):
        possible_moves = []
        row = self.square // 8
        col = self.square % 8

        directions = [
            (1, 0),   # Down
            (-1, 0),  # Up
            (0, 1),   # Right
            (0, -1),  # Left
            (1, 1),   # Down-right
            (1, -1),  # Down-left
            (-1, 1),  # Up-right
            (-1, -1)  # Up-left
        ]
        
        for direction in directions:
            r, c = row + direction[0], col + direction[1]
            if 0 <= r < 8 and 0 <= c < 8:
                possible_moves.append(r * 8 + c)
        
        return possible_moves