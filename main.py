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


# TODO: Need to mention target_piece, row, and col before using them
# TODO: Need to check position of pieces. Fix "self.position"

class ChessPiece:
    def __init__(self, symbol, color, image_path):
        self.symbol = symbol
        self.color = color
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.position = None  # To track the piece's position

    def get_symbol(self):
        return self.symbol

    def get_color(self):
        return self.color

    def get_image(self):
        return self.image

    def set_position(self, position):
        self.position = position


class King(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('K', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        current_row, current_col = self.position

        # Define all possible directions for the King to move
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                if not target_piece or target_piece.color != self.color:
                    moves.append((new_row, new_col))

        return moves
        pass  # TODO: Needs logic for the "castling" rule


class Rook(ChessPiece):
    def __init__(self, color, image_path):
        super().__init__('R', color, image_path)
        self.position = None

    def get_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # vertical and horizontal movement

        current_row, current_col = self.position

        for dr, dc in directions:
            for i in range(1, 8):  # Rook can move up to 7 squares in any direction
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


# Empty array for each respective colour's captured pieces
captured_white = []
captured_black = []

# Window for the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")


class ChessBoard:
    def __init__(self):
        self.piece_map = None
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
        self.whiteTurnMove = True  # whiteTurnMove = False means that it is black
        self.MoveLog = []  # tracks and prints all the moves in the terminal

    def get_piece_at(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            piece_symbol = self.board[row][col]
            if piece_symbol == "--":  # Check if it's an empty square
                return None

            piece_map = {
                "bR": Rook("black", "images/black_rook.png"),
                "bN": Knight("black", "/images/black_knight.png"),
                "bB": Bishop("black", "/images/black_bishop.png"),
                "bQ": Queen("black", "/images/black_queen.png"),
                "bK": King("black", "images/black_king.png"),
                "bP": Pawn("black", "/images/black_pawn.png"),
                "wR": Rook("white", "images/white_rook.png"),
                "wN": Knight("white", "/images/white_knight.png"),
                "wB": Bishop("white", "/images/white_bishop.png"),
                "wQ": Queen("white", "/images/white_queen.png"),
                "wK": King("white", "images/white_king.png"),
                "wP": Pawn("white", "/images/white_pawn.png"),
            }

            # If the piece symbol is in the map, return the corresponding piece
            if piece_symbol in piece_map:
                piece = piece_map[piece_symbol]
                piece.set_position((row, col))
                return piece
        return None

    def move_piece(self, move):  # executes moves as a parameter
        self.board[move.startRow][move.startCol] = ""  # square behind must be empty
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.MoveLog.append(move)  # create a move log to be able to undo moves
        self.whiteTurnMove = not self.whiteTurnMove  # swap player turn

    def undo_move(self):
        if len(self.MoveLog) != 0:  # Check that move log is not 0
            move = self.MoveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved  # reset the moved piece.
            self.board[move.endRow][move.endCol] = move.pieceCaptured  # reset the captured piece
            self.whiteTurnMove = not self.whiteTurnMove  # switch the turn back

    # Move code perhaps?
    def remove_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = ""
        pass  # TODO: Add remove piece function on the board


# Initialize that no column is being clicked
clicked_col = None

# Initialize ChessBoard
chess_board = ChessBoard()


class Move():
    # making new map key values
    # key : value
    # new keyvalues are: In chess rows are called ranks
    # Columns are called files in chess. I will change names and map key values to chess language from prog language
    # e.g. instead of black rook, positioned on row 0 col 0 (progr language) it is on rank 8 file 8 (chess language)

    rankToRow = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowToRank = {v: k for k, v in rankToRow.items()}  # for loop that reverses the values above, the other way around

    filesToCol = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
    colToFiles = {v: k for k, v in filesToCol.items()}

    def __init__(self, start_square, end_square, board):
        self.startRow = start_square[0]  # keep track of the data
        self.startCol = start_square[1]  # from this row, col
        self.endRow = end_square[0]  # to this row, col
        self.endCol = end_square[1]
        self.pieceMoved = board[self.startRow][self.startCol]  # move piece
        self.pieceCaptured = board[self.endRow][self.endCol]  # capture piece
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol  # Check note


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
