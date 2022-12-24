"""Class implementing a hexagonal grid with
axial coordinates."""

from typing import Tuple, Iterator

import numpy as np


Coordinate = Tuple[int, int]

DIRECTIONS = {
    #       q   r   s           q   r   s
    'UL': ( 0, -1,  1), 'UR': ( 1, -1,  0),
    'L':  (-1,  0,  1), 'R':  ( 1,  0, -1),
    'DL': (-1,  1,  0), 'DR': ( 0,  1, -1)
}


class HexagonalGrid:
    """Class encapsulating the hexagonal grid where
    the game occurs. Grid represented as a cubic
    array with dimensions max_size x max_size x 2.
    The first two dimensions represent the grid,
    while the last dimension represents:
        
        - in its first dimension, the occupancies
          of the grid (0 for empty, -1 hole,
          N for the player occupying the cell).
        - in its second dimension, the number of
          pieces in the cell."""

    def __init__(self, size: int, holes: Iterator[Coordinate]= None) -> None:
        self._size = size
        self._grid = np.zeros((size, size, 2), dtype=np.int8)
        if holes:
            for x, y in holes:
                self._grid[x, y, 0] = -1

    def get_size(self) -> int:
        """Returns the size of the grid."""
        return self._size

    def get_state(self) -> np.ndarray:
        """Returns the state of the grid."""
        return self._grid

    def get_score(self, player_id: int) -> int:
        """Returns the score of the grid."""
        return (self._grid[:, :, 0] == player_id).sum()

    @staticmethod
    def cube_to_offset(q: int, r: int, s: int) -> Tuple[int, int]:
        """Converts cube coordinates to offset coordinates."""
        assert q + r + s == 0, 'Wrong coordinates'
        x = r
        y = q + (r - (r & 1)) // 2
        return x, y

    @staticmethod
    def offset_to_cube(x: int, y: int) -> Tuple[int, int, int]:
        """Converts offset coordinates to cube coordinates."""
        q = y - (x - (x & 1)) // 2
        r = x
        s = -q - r
        return q, r, s

    def to_cube(self, x: int, y: int) -> Tuple[int, int, int]:
        """Converts offset coordinates to cube coordinates."""
        x -= self._size // 2
        y -= self._size // 2
        q, r, s = HexagonalGrid.offset_to_cube(x, y)
        return q, r, s

    def to_offset(self, q: int, r: int, s: int) -> Tuple[int, int]:
        """Converts cube coordinates to offset coordinates."""
        x, y = HexagonalGrid.cube_to_offset(q, r, s)
        x += self._size // 2
        y += self._size // 2
        return x, y

    def __getitem__(self, q: int, r: int, s: int) -> np.ndarray:
        x, y = self.to_offset(q, r, s)
        return self._grid[x, y]

    def _out_of_bounds(self, q: int, r: int, s: int) -> bool:
        """Returns True if the given coordinates are out of bounds."""
        x, y = self.to_offset(q, r, s)
        return x < 0 or x >= self._size or y < 0 or y >= self._size

    def is_empty(self, q: int, r: int, s:int) -> bool:
        """Returns True if the cell is empty."""
        return self.__getitem__(q, r, s)[0] == 0 

    def is_hole(self, q: int, r: int, s: int) -> bool:
        """Returns True if the cell is a hole."""
        return self.__getitem__(q, r, s)[0] == -1 

    def is_occupied(self, q: int, r: int, s: int) -> bool:
        """Returns True if the cell is occupied."""
        return self.__getitem__(q, r, s)[0] > 0 

    def is_occupied_by_player(self, q: int, r: int, s: int, player_id: int) -> bool:
        """Returns True if the cell is occupied."""
        return self.__getitem__(q, r, s)[0] == player_id

    def player_at(self, q: int, r: int, s: int) -> int:
        """Returns the player occupying the cell. Will
        raise an AssertionError if the cell is not occupied."""
        assert self.is_occupied(q, r, s)
        return self.__getitem__(q, r, s)[0]

    def units_at(self, q: int, r: int, s: int) -> int:
        """Returns the number of units in the cell. Will
        raise an AssertionError if the cell is not occupied."""
        assert self.is_occupied(q, r, s)
        return self.__getitem__(q, r, s)[1] 

    def get_player_positions(self, player_id: int) -> Iterator[Coordinate]:
        """Returns an iterator of the positions of the
        given player."""
        assert player_id >= 1
        return np.where(self._grid[..., 0] == player_id)

    def get_next_moveable_cell(self, q: int, r: int, s: int, direction: str) -> Coordinate:
        """Returns the next cell in the grid in the given
        direction that a player can move to."""
        if direction not in DIRECTIONS.keys():
            raise ValueError('Invalid direction.')

        dq, dr, ds = DIRECTIONS[direction]
        while not self._out_of_bounds(q+dq, r+dr, s+ds):
            if not self.is_empty(q+dq, r+dr, s+ds):
                return q, r, s
            q += dq
            r += dr
            s += ds
        return q, r, s

    def get_moveable_positions(self) -> Iterator[Coordinate]:
        """Returns an iterator of the positions where it
        is still possible to move."""
        return np.where(self._grid[..., 1] > 1).T

    def get_player_moveable_positions(self, player_id: int) -> Iterator[Coordinate]:
        """Returns an iterator of the positions of the
        given player that can be moved."""
        assert player_id >= 1
        player_options = np.vstack(np.where(
            (self._grid[..., 0] == player_id) &
            (self._grid[..., 1] > 1))).T
        return [(q, r, s) for q, r, s in player_options
            if self._available_moves(q, r, s)]

    def _available_moves(self, q: int, r: int, s: int) -> bool:
        """Returns True if the cell can be moved."""
        # For efficiency, check neighbours first
        for direction in DIRECTIONS.keys():
            dq, dr, ds = DIRECTIONS[direction]
            if self._out_of_bounds(q+dq, r+dr, s+ds):
                continue
            if self.is_empty(q+dq, r+dr, s+ds):
                return True

        # Then check the rest
        for direction in DIRECTIONS.keys():
            nq, nr, ns = self.get_next_moveable_cell(q, r, s, direction)
            if np.any([nq != q, nr != r, ns != s]):
                return True

        return False

    def initialize_player(self, player_id: int, q: int, r: int, s: int,
    n_units: int) -> None:
        """Initializes the player at the given coordinates."""
        assert self.is_empty(q, r, s)
        assert player_id >= 1
        x, y = self.to_offset(q, r, s)
        self._grid[x, y, 0] = player_id 
        self._grid[x, y, 1] = n_units 

    def move_player(self, player_id: int, x: int, y: int,
    n_units: int, direction: str) -> None:
        """Moves the player in the given direction."""
        q, r, s = self.to_cube(x, y)
        assert player_id >= 1
        assert self.player_at(q, r, s) == player_id
        assert n_units > 1 and n_units < self.units_at(q, r, s)
        nq, nr, ns = self.get_next_moveable_cell(q, r, s, direction)
        assert self.is_empty(nq, nr, ns) and (nq != q or nr != r or ns != s)

        nx, ny = self.to_offset(nq, nr, ns)
        self._grid[x, y, 1] -= n_units      
        self._grid[nx, ny, 0] = player_id
        self._grid[nx, ny, 1] = n_units
