"""Classes representing the state of the board."""


from typing import Iterator, List

import numpy as np
from coordinate import Coordinate

DIRECTIONS = {
    'UR': Coordinate( 1,  1), 'UL': Coordinate( 1, -1),
    'R':  Coordinate( 0,  1),  'L': Coordinate( 0, -1),
    'DR': Coordinate(-1, -1), 'DL': Coordinate(-1, -1)
}


class Board:
    """Class representing the state of the board
    at any given point of the game. This class
    encapsulates the grid and the pieces on it.
    
    Internally, the grid is represented as a cubic
    array with dimensions max_size x max_size x 3.
    The first two dimensions represent the grid,
    while the last dimension represents:
        
        - in its first dimension, the occupancies
          of the grid (0 for empty, -1 hole,
          N for the player occupying the cell).
        - in its second dimension, the number of
          pieces in the cell.

    Parameters:

        - size: the size of the grid.
        - holes: an iterator of coordinates of the holes
            in the grid.

    Functions:
        - is_empty: returns True if the cell is empty.
        - is_hole: returns True if the cell is a hole.
        - is_occupied: returns True if the cell is occupied.
        - player_at: returns the player occupying the cell.
        - next_empty_cell: returns the next empty cell
     """

    def __init__(self, size: int, holes: Iterator[Coordinate]= None) -> None:
        self._grid = np.zeros((size, size, 2), dtype=np.int8)
        if holes:
            for x, y in holes:
                self._grid[x, y, 0] = -1

    def get_state(self) -> np.ndarray:
        """Returns the state of the board."""
        return self._grid

    def get_score(self, player) -> int:
        return len(self._grid[..., 0] == player)

    def is_empty(self, c: Coordinate) -> bool:
        """Returns True if the cell is empty."""
        return self._grid[c][0] == 0 # type: ignore

    def is_hole(self, c: Coordinate) -> bool:
        """Returns True if the cell is a hole."""
        return self._grid[c][0] == -1 # type: ignore

    def is_occupied(self, c: Coordinate) -> bool:
        """Returns True if the cell is occupied."""
        return self._grid[c][0] > 0 # type: ignore

    def player_at(self, c: Coordinate) -> int:
        """Returns the player occupying the cell. Will
        raise an AssertionError if the cell is not occupied."""
        assert self.is_occupied(c)
        return self._grid[c][0] # type: ignore

    def units_at(self, c: Coordinate) -> int:
        """Returns the number of units in the cell. Will
        raise an AssertionError if the cell is not occupied."""
        assert self.is_occupied(c)
        return self._grid[c][1] # type: ignore

    def get_player_positions(self, player: int) -> Iterator[Coordinate]:
        """Returns an iterator of the positions of the
        given player."""
        return np.where(self._grid[..., 0] == player)

    def initialize_player(self, player: int, c: Coordinate, n_units: int) -> None:
        """Initializes the player at the given coordinates."""
        assert self.is_empty(c)
        self._grid[c][0] = player  # type: ignore
        self._grid[c][1] = n_units # type: ignore

    def next_empty_cell(self, c: Coordinate, direction: str) -> Coordinate:
        """Returns the next empty cell in the grid, starting from the given
        coordinates."""
        if direction not in DIRECTIONS.keys():
            return ValueError('Invalid direction.')

        dc = DIRECTIONS[direction]
        while self[(c+dc)] == 0: # type: ignore
            c += dc
        return c

    def move_player(self, player: int, c: Coordinate, n_units: int, direction: str) -> None:
        """Moves the player at the given coordinates."""
        assert self.player_at(c) == player
        assert n_units > 1 and n_units < self.units_at(c) - 1
        next_c = self.next_empty_cell(c, direction)
        assert self.is_empty(next_c) and next_c != c

        self._grid[c][1] -= n_units      # type: ignore
        self._grid[next_c][0] = player   # type: ignore
        self._grid[next_c][1] = n_units  # type: ignore

    def get_player_moveable_positions(self, player: int) -> Iterator[Coordinate]:
        """Returns an iterator of the positions of the
        given player that can be moved."""
        player_options = np.where(self._grid[..., 0] == player and self._grid[..., 1] > 1)
        return [option for option in player_options
            if self._available_moves(option)]

    def _available_moves(self, c: Coordinate) -> bool:
        """Returns True if the cell can be moved."""
        # For efficiency, check neighbours first
        for _, dc in DIRECTIONS.items():
            if self._grid[(c+dc)][0]== 0: # type: ignore
                return True

        # Then check the rest
        for direction in DIRECTIONS.keys():
            if self.next_empty_cell(c, direction) != c:
                return True

        return False

    def get_moveable_positions(self) -> Iterator[Coordinate]:
        """Returns an iterator of the positions where it
        is still possible to move."""
        return np.where(self._grid[..., 1] > 1)
