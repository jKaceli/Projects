from enum import Enum
from player import Player
from move import Move
from chess_piece import ChessPiece
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
from move import Move

class MoveValidity(Enum):
    Valid = 1
    Invalid = 2
    MovingIntoCheck = 3
    StayingInCheck = 4

    def __str__(self):
        if self.value == 2:
            return 'Invalid move.'

        if self.value == 3:
            return 'Invalid -- cannot move into check.'

        if self.value == 4:
            return 'Invalid -- must move out of check.'


class UndoException(Exception):
    pass


class ChessModel:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]  # Initialize an empty board
        self.__player = Player.WHITE  # Start with white player
        self.__nrows = 8
        self.__ncols = 8
        self.__message_code = None
        self.moves_history = []

    @property
    def nrows(self) -> int:
        return self.__nrows

    @property
    def ncols(self) -> int:
        return self.__ncols

    @property
    def current_player(self) -> Player:
        return self.__player

    @property
    def message_code(self) -> MoveValidity:
        return self.__message_code

    def is_complete(self) -> bool:
        # Logic to check if the game is complete (e.g., checkmate)
        pass

    def is_valid_move(self, move: Move) -> bool:
        piece = self.piece_at(move.start[0], move.start[1])
        if piece is None or piece.player != self.__player:
            return MoveValidity.Invalid

        if move.end[0] < 0 or move.end[0] >= self.__nrows or move.end[1] < 0 or move.end[1] >= self.__ncols:
            return MoveValidity.Invalid

        if move.start == move.end:
            return MoveValidity.Invalid

        if not piece.is_valid_move(move, self.board):
            return MoveValidity.Invalid

        # Simulate the move and check if the player is still in check
        self.simulate_move(move)
        if self.in_check(self.__player):
            self.undo_last_move()
            return MoveValidity.StayingInCheck

        # Check if moving would put the player in check
        opponent = Player.WHITE if self.__player == Player.BLACK else Player.BLACK
        if self.in_check(opponent):
            self.undo_last_move()
            return MoveValidity.MovingIntoCheck

        self.undo_last_move()
        return MoveValidity.Valid

    def move(self, move: Move):
        if self.is_valid_move(move) == MoveValidity.Valid:
            piece = self.piece_at(move.start[0], move.start[1])
            self.board[move.end[0]][move.end[1]] = piece
            self.board[move.start[0]][move.start[1]] = None
            self.moves_history.append(move)
            self.set_next_player()

    def in_check(self, p: Player) -> bool:
        king_pos = self.find_king(p)
        for row in range(self.__nrows):
            for col in range(self.__ncols):
                piece = self.piece_at(row, col)
                if piece is not None and piece.player != p and (row, col) != king_pos:
                    if piece.is_valid_move(Move((row, col), king_pos), self.board):
                        return True
        return False

    def find_king(self, p: Player) -> Tuple[int, int]:
        for row in range(self.__nrows):
            for col in range(self.__ncols):
                piece = self.piece_at(row, col)
                if isinstance(piece, King) and piece.player == p:
                    return row, col
        raise ValueError("King not found on the board.")

    def piece_at(self, row: int, col: int) -> ChessPiece:
        return self.board[row][col]

    def set_next_player(self):
        self.__player = Player.WHITE if self.__player == Player.BLACK else Player.BLACK

    def set_piece(self, row: int, col: int, piece: ChessPiece):
        if row < 0 or row >= self.__nrows or col < 0 or col >= self.__ncols:
            raise ValueError("Row or column out of bounds.")
        if not isinstance(piece, ChessPiece):
            raise TypeError("Invalid piece type.")
        self.board[row][col] = piece

    def undo(self):
        if len(self.moves_history) == 0:
            raise UndoException("No moves to undo")

        last_move = self.moves_history.pop()
        self.board[last_move.start[0]][last_move.start[1]] = self.board[last_move.end[0]][last_move.end[1]]
        self.board[last_move.end[0]][last_move.end[1]] = None
        self.set_next_player()

    def simulate_move(self, move: Move):
        piece = self.piece_at(move.start[0], move.start[1])
        self.board[move.end[0]][move.end[1]] = piece
        self.board[move.start[0]][move.start[1]] = None

    def undo_last_move(self):
        last_move = self.moves_history[-1]
        self.board[last_move.start[0]][last_move.start[1]] = self.board[last_move.end[0]][last_move.end[1]]
        self.board[last_move.end[0]][last_move.end[1]] = None
