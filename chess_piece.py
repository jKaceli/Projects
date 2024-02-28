from enum import Enum
from abc import ABC, abstractmethod
from typing import List
from chess_model import Move


class Player(Enum):
    WHITE = 0
    BLACK = 1


class ChessPiece(ABC):
    def __init__(self, player: Player):
        self.__player = player

    @property
    def player(self) -> Player:
        return self.__player

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        start_row, start_col = move.start
        end_row, end_col = move.end

        # Verify indices associated with move are in bounds
        if not (0 <= start_row < len(board) and 0 <= start_col < len(board[0]) and 0 <= end_row < len(
                board) and 0 <= end_col < len(board[0])):
            return False

        # Verify starting and ending locations are different
        if move.start == move.end:
            return False

        # Verify that self piece is located at starting location in move
        if board[start_row][start_col] != self:
            return False

        # Verify that ending location does not contain a piece belonging to the same player as self piece
        if board[end_row][end_col] is not None and board[end_row][end_col].player == self.player:
            return False

        return True

