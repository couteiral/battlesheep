"""Utils to build initial board."""

import random
from typing import Iterator

import numpy as np

from grid import HexagonalGrid, DIRECTIONS    


class HexCoord:
    """Class representing a coordinate in a hexagonal grid."""

    def __init__(self, q: int, r: int, s: int):
        assert q + r + s == 0
        self.q = q
        self.r = r
        self.s = s

    def __add__(self, other: 'HexCoord') -> 'HexCoord':
        return HexCoord(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other: 'HexCoord') -> 'HexCoord':
        return HexCoord(self.q - other.q, self.r - other.r, self.s - other.s)

    def __repr__(self) -> str:
        return f'HexCoord({self.q}, {self.r}, {self.s})'

    def __eq__(self, other: 'HexCoord') -> bool:
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __hash__(self) -> int:
        return hash((self.q, self.r, self.s))

    def __iter__(self) -> Iterator[int]:
        return iter((self.q, self.r, self.s))


def _join_two_tiles(one: Iterator[HexCoord], other: Iterator[HexCoord],
                   c1: HexCoord, c2: HexCoord, rel_direction: str) -> Iterator[HexCoord]:    
    assert rel_direction in DIRECTIONS
    new_space_occupied = one.copy()
    dir_vector = HexCoord(*DIRECTIONS[rel_direction])
    for c in other:
        new_space_occupied.append(c1 + (c - c2) + dir_vector)
    if len(new_space_occupied) > len(set(new_space_occupied)):
        raise ValueError('Tiles overlap.')
    else:
        return new_space_occupied

def _try_join_tiles(one: Iterator[HexCoord], other: Iterator[HexCoord],
                   c1: HexCoord, c2: HexCoord, rel_direction: str) -> Iterator[HexCoord]:    
    try:
        return _join_two_tiles(one, other, c1, c2, rel_direction)
    except ValueError:
        return None


class HexagonalTile:
    """Class abstracting an hexagonal tile
    or a collection of stacked hexagonal tiles."""

    def join(self, other: 'HexagonalTile', c1: HexCoord, c2: HexCoord,
             rel_direction: str) -> 'HexagonalTile':
        """Joins the given tile to the current one."""
        assert rel_direction in DIRECTIONS
        new_space_occupied = _try_join_tiles(self.space_occupied, other.space_occupied,
                                             c1, c2, rel_direction)
        if new_space_occupied is None:
            raise ValueError('Tiles do not match.')
        else:
            self.space_occupied = new_space_occupied
            return self

    def to_square_grid(self) -> np.ndarray:
        """Converts the tile to a square grid."""
        x, y = [], []
        for q, r, s in self.space_occupied:
            x_, y_ = HexagonalGrid.cube_to_offset(q, r, s)
            x.append(x_); y.append(y_)
        x = np.array(x); y = np.array(y)
        x -= x.min(); y -= y.min()

        square_grid = -1. * np.ones((x.max() + 1, y.max() + 1), dtype=np.int8)
        square_grid[x, y] = 0
        return square_grid
    

class SingleHexagon(HexagonalTile):
    """Class representing a single hexagon."""
    
    def __init__(self):
        self.space_occupied = [
            HexCoord( 0,  0,  0),
        ]
    

class BasicTile(HexagonalTile):
    """Class representing a single hexagon."""
    
    def __init__(self):
        self.space_occupied = [
            HexCoord( 0,  0,  0),
            HexCoord( 0, -1,  1),
            HexCoord( 1, -1,  0),
            HexCoord( 1,  0, -1),
        ]

def generate_random_tiling(n_basic_tiles, max_tries=100, max_picks=20):
    """Generates a random tiling of hexagonal tiles."""

    n_tries = 0
    while n_tries < max_tries:
        n_tries += 1

        construction = BasicTile()
        for _ in range(n_basic_tiles):
            n_picks = 0
            succeeded = False
            while n_picks < max_picks:
                n_picks += 1
                try:
                    new_tile = BasicTile()
                    c1 = random.choice(construction.space_occupied)
                    c2 = random.choice(new_tile.space_occupied)
                    rel_direction = random.choice([k for k in DIRECTIONS.keys()])
                    construction = construction.join(
                        new_tile, c1, c2, rel_direction
                    )
                    succeeded = True
                    break
                except ValueError as e:
                    pass

            if not succeeded:
                break

    return construction
            