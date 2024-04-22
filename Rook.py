from main import ChessPiece


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
