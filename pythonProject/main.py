import pygame
import sys

# Initialize
pygame.init()

# Definition of constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
timer = pygame.time.Clock()
fps = 60

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class ChessPiece:
    def __init__(self, symbol, color, image_path):
        self.symbol = symbol
        self.color = color
        self.image_path = image_path
        self.image = pygame.image.load(image_path)

    def get_symbol(self):
        return self.symbol

    def get_color(self):
        return self.color

    def get_image(self):
        return self.image


class King(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('K', color, image_path)
        
    def get_moves(self, board):
        moves = []
        current_row, current_col = self.position

        # Define all possible directions for the King to move
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]
        pass  # Needs move set for the King, including "castling"


class Queen(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('Q', color, image_path)

    def get_moves(self, board):
        pass  # Needs move set for the Queen


class Rook(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('R', color, image_path)

    def get_moves(self, board):
        return  # Needs move set for the Rooks


class Bishop(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('B', color, image_path)

    def get_moves(self, board):
        pass  # Needs move set for the Bishops


class Knight(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('N', color, image_path)

    def get_moves(self, board):
        pass  # Needs move set for the Knights


class Pawn(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('P', color, image_path)

    def get_moves(self, board):
        pass  # Needs move set for the Pawns, including "en passant"


# Create chess board with all piece's start position, global variables
white_pieces = [
    King('white', 'images/white_king.png'),
    Queen('white', 'images/white_queen.png'),
    Rook('white', 'images/white_rook.png'),
    Bishop('white', 'images/white_bishop.png'),
    Knight('white', 'images/white_knight.png'),
    Pawn('white', 'images/white_pawn.png')
]

black_pieces = [
    King('black', 'images/black_king.png'),
    Queen('black', 'images/black_queen.png'),
    Rook('black', 'images/black_rook.png'),
    Bishop('black', 'images/black_bishop.png'),
    Knight('black', 'images/black_knight.png'),
    Pawn('black', 'images/black_pawn.png')
]
captured_white = []
captured_black = []

# Window for the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")


class ChessBoard:
    def __init__(self):
        self.board = [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "q", "k", "b", "n", "r"],
        ]

    def get_piece_at(self, board):
        if 0 <= row < 8 and 0 <= col < 8:
            piece_symbol = self.board[row][col]
            if piece_symbol:
                color = "white" if piece_symbol.isupper() else "black"
                return globals()[piece_symbol.capitalize()](color)
        return None


# Initialize that no column is being clicked
clicked_col = None

# Initialize ChessBoard
chess_board = ChessBoard()

# Game loop
while True:
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Inside the game loop, after the event handling loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_row = mouse_pos[1] // SQUARE_SIZE
            clicked_col = mouse_pos[0] // SQUARE_SIZE
            clicked_piece = chess_board.get_piece_at(clicked_row, clicked_col)

            if clicked_piece:
                selected_piece = clicked_piece
            else:
                selected_piece = None

            if selected_piece:
                target_piece = chess_board.get_piece_at(clicked_row, clicked_col)
                if target_piece:
                    # ^If there is already a piece in the target square, implement capture logic here
                    pass
                else:
                    # Move the selected piece to the empty square
                    selected_piece.move_to(clicked_row, clicked_col)

    # For-loop to check right square to set the colour
    for row in range(8):
        for col in range(8):
            square_color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # For-loop to check each square to place the right piece
    for row in range(8):
        for col in range(8):
            piece = chess_board.get_piece_at(row, col)
            if piece:
                screen.blit(piece.get_image(), (col * SQUARE_SIZE, row * SQUARE_SIZE))

    selected_piece = None

    # Update Display
    pygame.display.flip()

# End game
pygame.quit()
