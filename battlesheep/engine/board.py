"""Classes representing the state of the board."""


from typing import Iterator, Tuple

import numpy as np

from .grid import Coordinate


Action = Tuple[Coordinate, str]


class Board:
    """Class representing the state of the board
    at any given point of the game, and providing
    functions to interact with it."""

    def __init__(self, size: int, holes: Iterator[Coordinate]= None) -> None:
        self._size = size
        self._grid = np.zeros((size, size, 2), dtype=np.int8)
        if holes:
            for x, y in holes:
                self._grid[x, y, 0] = -1

    def _out_of_bounds(self, c):
        return c < 0 or c >= self._size

    def get_size(self) -> int:
        """Returns the size of the grid."""
        return self._grid.get_size()

    def get_state(self) -> np.ndarray:
        """Returns the state of the board."""
        return self._grid.get_state()

    def get_score(self, player_id) -> int:
        assert player_id >= 1
        return len(self._grid[..., 0] == player_id)

    def move_player(self, player_id: int, x: int, y: int, n_units: int, direction: str) -> None:
        """Moves the player at the given coordinates."""
        assert player_id >= 1
        assert self.player_at(x, y) == player_id
        assert n_units > 1 and n_units < self.units_at(x, y)
        nx, ny = self.next_empty_cell(x, y, direction)
        assert self.is_empty(nx, ny) and (nx != x or ny != ny)

        self._grid[x, y, 1] -= n_units      
        self._grid[nx, ny, 0] = player_id
        self._grid[nx, ny, 1] = n_units  

    def _get_actions(self, player_id: int) -> Iterator[Action]:
        """Returns an iterator of the actions that the
        given player can perform."""
        assert player_id >= 1
        for x, y in self.get_player_moveable_positions(player_id):
            for direction in DIRECTIONS.keys():
                nx, ny = self.next_empty_cell(x, y, direction)
                if x != nx or y != ny:
                    yield (x, y), direction

    def get_actions(self, player_id: int) -> Iterator[Action]:
        """Returns an iterator of the actions that the
        given player can perform."""
        assert player_id >= 1
        return [action for action in self._get_actions(player_id)]

