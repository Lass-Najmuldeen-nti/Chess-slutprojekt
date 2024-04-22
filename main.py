import pygame
import sys
import King, Rook

import self

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


# TODO: Need to mention target_piece, row, and col before using them
# TODO: Need to check position of pieces. Fix "self.position"

class ChessPiece:
    def __init__(self, symbol, color, image_path):
        self.symbol = symbol
        self.color = color
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.position = None

    def get_symbol(self):
        return self.symbol

    def get_color(self):
        return self.color

    def get_image(self):
        return self.image

    def set_position(self, position):
        self.position = position


class Queen(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('Q', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),  # vertical and horizontal movement
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]  # diagonal movement

        current_row, current_col = self.position

        for dr, dc in directions:
            for i in range(1, 8):  # Queen can move up to 7 squares in any direction
                new_row, new_col = current_row + i * dr, current_col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board.get_piece_at(new_row, new_col)
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece.color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break
        return moves
        pass


class Bishop(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('B', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]  # diagonal

        current_row, current_col = self.position

        for dr, dc in directions:
            for i in range(1, 8):  # Bishop can move up to 7 squares in any direction
                new_row, new_col = current_row + i * dr, current_col + i * dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board.get_piece_at(new_row, new_col)
                    if not target_piece:
                        moves.append((new_row, new_col))
                    elif target_piece.color != self.color:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break
                else:
                    break

        return moves
        pass


class Knight(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('N', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        # tuples for the knight
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]

        current_row, current_col = self.position

        for dr, dc in offsets:
            new_row, new_col = current_row + dr, current_col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                if not target_piece or target_piece.color != self.color:
                    moves.append((new_row, new_col))

        return moves
        pass


class Pawn(ChessPiece):
    # Previous move coordinates
    previous_move = None

    def __init__(self, color, image_path):
        super().__init__('P', color, image_path)
        self.position = None
        self.starting_row = None  # Define position and starting row

    def get_moves(self, board):
        moves = []
        current_row, current_col = self.position

        # Define the direction in which the pawn moves based on its color
        direction = 1 if self.color == 'white' else -1

        # Check one square ahead
        if 0 <= current_row + direction < 8:
            if not board.get_piece_at(current_row + direction, current_col):
                moves.append((current_row + direction, current_col))

                # Check two squares ahead if it's the pawn's starting position
                if current_row == self.starting_row and not board.get_piece_at(current_row + 2 * direction,
                                                                               current_col):
                    moves.append((current_row + 2 * direction, current_col))

        # Check diagonal squares for capturing
        for col_offset in [-1, 1]:
            new_row = current_row + direction
            new_col = current_col + col_offset
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                if target_piece and target_piece.color != self.color:
                    moves.append((new_row, new_col))
                elif target_piece is None and (new_row, new_col) == self.previous_move:
                    moves.append((new_row, new_col))

        return moves
        pass  # TODO: Needs logic for the "en passant" rule


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
        # Initialize the position of each piece
        self.initialize_pieces()

    def initialize_pieces(self):
        piece_map = {
            "r": Rook("black", "images/black_rook.png"),
            "n": Knight("black", "images/black_knight.png"),
            "b": Bishop("black", "images/black_bishop.png"),
            "q": Queen("black", "images/black_queen.png"),
            "k": King("black", "images/black_king.png"),
            "p": Pawn("black", "images/black_pawn.png"),
            "R": Rook("white", "images/white_rook.png"),
            "N": Knight("white", "images/white_knight.png"),
            "B": Bishop("white", "images/white_bishop.png"),
            "Q": Queen("white", "images/white_queen.png"),
            "K": King("white", "images/white_king.png"),
            "P": Pawn("white", "images/white_pawn.png"),
        }

    # Rethink the colouring process
    def get_piece_at(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            piece_symbol = self.board[row][col]
            if piece_symbol:
                color = "white" if piece_symbol.isupper() else "black"
                return globals()[piece_symbol.capitalize()](color)  # Should return the piece at the specified position
                # But it's returning a new piece instance bas ed on the position without considering the actual piece
                # on the board.
        return None
        pass

    # Move code perhaps?
    def remove_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = ""
        pass  # TODO: Add remove piece function on the board


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

        # Check if mouse is being clicked and where it is selecting
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
                    # Capture the target piece if it exists and it's of the opposite color
                    if target_piece.color != selected_piece.color:
                        # Check if the selected piece is capable of capturing the target piece
                        if (clicked_row, clicked_col) in selected_piece.get_moves(chess_board):
                            target_piece.position = None  # Reset target piece position
                            chess_board.remove_piece(clicked_row, clicked_col)  # Remove the captured piece
                            selected_piece.move_to(clicked_row, clicked_col)

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
# pygame.quit()
