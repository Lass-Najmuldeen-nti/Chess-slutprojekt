

from main import ChessPiece


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
