"""Main game engine."""

from typing import Iterator

import numpy as np

from board import Board
from coordinate import Coordinate


class GameEnvironment:

    def __init__(self, size: int, n_players: int,
    holes: Iterator[Coordinate]) -> None:
        self._board = Board(size, holes)
        self._n_players = n_players

    def initialize(self, init: dict):
        """Initializes the game."""
        for player, (c, n_units) in init.items():
            self._board.initialize_player(player, c, n_units)

    def get_state(self) -> np.ndarray:
        """Returns the state of the board."""
        return self._board.get_state()

    def get_actions(self, player: int) -> Iterator[Coordinate]:
        """Returns an iterator of the actions
        available to the player."""
        return self._board.get_player_moveable_positions(player)

    def get_score(self, player: int) -> int:
        """Returns the score of the player."""
        return self._board.get_score(player)

    def make_move(self, player: int, c: Coordinate, direction: str) -> None:
        """Makes a move for the given player."""
        self._board.move_player(player, c, direction)
