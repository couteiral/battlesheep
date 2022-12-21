"""Classes representing the state of the board."""


from typing import Iterator, Tuple

import numpy as np

Coordinate = Tuple[int, int]
Action = Tuple[Coordinate, str]

DIRECTIONS = {
    'UR': ( 0,  1), 'UL': (-1, -1),
    'R':  ( 0,  1),  'L': ( 0, -1),
    'DR': ( 0, -1), 'DL': (-1, -1)
}

def _calculate_delta(x: int, y: int, direction: str) -> Coordinate:
    """Returns the delta of the given direction."""
    dx, dy = DIRECTIONS[direction]
    if y % 2 == 1:
        dx = dx + 1
    return dx, dy


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
        self._size = size
        self._grid = np.zeros((size, size, 2), dtype=np.int8)
        if holes:
            for x, y in holes:
                self._grid[x, y, 0] = -1

    def _out_of_bounds(self, c):
        return c < 0 or c >= self._size

    def get_size(self) -> int:
        """Returns the size of the grid."""
        return self._size

    def get_state(self) -> np.ndarray:
        """Returns the state of the board."""
        return self._grid

    def get_score(self, player_id) -> int:
        return len(self._grid[..., 0] == player_id)

    def is_empty(self, x: int, y: int) -> bool:
        """Returns True if the cell is empty."""
        return self._grid[x, y, 0] == 0 

    def is_hole(self, x: int, y: int) -> bool:
        """Returns True if the cell is a hole."""
        return self._grid[x, y, 0] == -1 

    def is_occupied(self, x: int, y: int) -> bool:
        """Returns True if the cell is occupied."""
        return self._grid[x, y, 0] > 0 

    def player_at(self, x: int, y: int) -> int:
        """Returns the player occupying the cell. Will
        raise an AssertionError if the cell is not occupied."""
        assert self.is_occupied(x, y)
        return self._grid[x, y, 0] 

    def units_at(self, x: int, y: int) -> int:
        """Returns the number of units in the cell. Will
        raise an AssertionError if the cell is not occupied."""
        assert self.is_occupied(x, y)
        return self._grid[x, y, 1] 

    def get_player_positions(self, player_id: int) -> Iterator[Coordinate]:
        """Returns an iterator of the positions of the
        given player."""
        return np.where(self._grid[..., 0] == player_id)

    def initialize_player(self, player_id: int, x: int, y: int, n_units: int) -> None:
        """Initializes the player at the given coordinates."""
        assert self.is_empty(x, y)
        self._grid[x, y, 0] = player_id 
        self._grid[x, y, 1] = n_units 

    def next_empty_cell(self, x: int, y: int, direction: str) -> Coordinate:
        """Returns the next empty cell in the grid, starting from the given
        coordinates."""
        if direction not in DIRECTIONS.keys():
            return ValueError('Invalid direction.')

        dx, dy = _calculate_delta(x, y, direction)
        while self._grid[x+dx, y+dy, 0] == 0: 
            x += dx; y += dy
            if self._out_of_bounds(x+dx) or self._out_of_bounds(y+dy):
                break
        return x, y

    def move_player(self, player_id: int, x: int, y: int, n_units: int, direction: str) -> None:
        """Moves the player at the given coordinates."""
        assert self.player_at(x, y) == player_id
        assert n_units > 1 and n_units < self.units_at(x, y) - 1
        nx, ny = self.next_empty_cell(x, y, direction)
        assert self.is_empty(nx, ny) and (nx != x or ny != ny)

        self._grid[x, y, 1] -= n_units      
        self._grid[nx, ny, 0] = player_id
        self._grid[nx, ny, 1] = n_units  

    def get_player_moveable_positions(self, player_id: int) -> Iterator[Coordinate]:
        """Returns an iterator of the positions of the
        given player that can be moved."""
        player_options = np.where(self._grid[..., 0] == player_id and self._grid[..., 1] > 1)
        return [option for option in player_options
            if self._available_moves(option)]

    def _get_actions(self, player_id: int) -> Iterator[Action]:
        """Returns an iterator of the actions that the
        given player can perform."""
        for x, y in self.get_player_moveable_positions(player_id):
            for direction in DIRECTIONS.keys():
                nx, ny = self.next_empty_cell(x, y, direction)
                if x != nx or y != ny:
                    yield (x, y), direction

    def get_actions(self, player_id: int) -> Iterator[Action]:
        """Returns an iterator of the actions that the
        given player can perform."""
        return [action for action in self._get_actions(player_id)]

    def _available_moves(self, x: int, y: int) -> bool:
        """Returns True if the cell can be moved."""
        # For efficiency, check neighbours first
        for direction in DIRECTIONS.keys():
            dx, dy = _calculate_delta(x, y, direction)
            if self._grid[x+dx, y+dy] == 0: 
                return True

        # Then check the rest
        for direction in DIRECTIONS.keys():
            nx, ny = self.next_empty_cell(nx, ny, direction)
            if x != nx or y != ny:
                return True

        return False

    def get_moveable_positions(self) -> Iterator[Coordinate]:
        """Returns an iterator of the positions where it
        is still possible to move."""
        return np.where(self._grid[..., 1] > 1)
