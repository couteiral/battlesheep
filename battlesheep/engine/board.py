"""Classes representing the state of the board."""


from typing import Iterator, Tuple

import numpy as np

from .grid import Coordinate, HexagonalGrid, DIRECTIONS


Action = Tuple[Coordinate, str]


class Board:
    """Class representing the state of the board
    at any given point of the game, and providing
    functions to interact with it."""

    def __init__(self, size: int, holes: Iterator[Coordinate]= None) -> None:
        self._grid = HexagonalGrid(size, holes)

    def get_size(self) -> int:
        """Returns the size of the grid."""
        return self._grid.get_size()

    def get_state(self) -> np.ndarray:
        """Returns the state of the board."""
        return self._grid.get_state()

    def get_score(self, player_id) -> int:
        assert player_id >= 1
        return self._grid.get_score(player_id)

    def is_hole(self, x: int, y: int) -> bool:
        """Returns True if the given cell is a hole."""
        return self._grid.is_hole(x, y)

    def is_empty(self, x: int, y: int) -> bool:
        """Returns True if the given cell is empty."""
        return self._grid.is_empty(x, y)

    def units_at(self, x: int, y: int) -> int:
        """Returns the number of units at the given cell."""
        return self._grid.units_at(x, y)

    def player_at(self, x: int, y: int) -> int:
        """Returns the player at the given cell."""
        return self._grid.player_at(x, y)

    def initialize_player(self, player_id: int, x: int, y: int, n_units: int) -> None:
        """Initializes the player at the given coordinates."""
        self._grid.initialize_player(player_id, x, y, n_units)

    def move_player(self, player_id: int, x: int, y: int,
    n_units: int, direction: str) -> None:
        """Moves the player at the given coordinates."""
        self._grid.move_player(player_id, x, y, n_units, direction)

    def _get_actions(self, player_id: int) -> Iterator[Action]:
        """Returns an iterator of the actions that the
        given player can perform."""
        for x, y in self._grid.get_player_moveable_positions(player_id):
            for direction in DIRECTIONS.keys():
                nx, ny = self._grid.get_next_moveable_cell(x, y, direction)
                if x != nx or y != ny:
                    yield (x, y), direction

    def get_actions(self, player_id: int) -> Iterator[Action]:
        """Returns an iterator of the actions that the
        given player can perform."""
        assert player_id >= 1
        return [action for action in self._get_actions(player_id)]

