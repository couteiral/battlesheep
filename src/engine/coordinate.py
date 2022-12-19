"""Class to represent coordinates."""

from typing import Iterator

import numpy as np


class Coordinate:
    """Class to represent the coordinates of a cell.
    Conceived to allow potentially more than 2 dimensions."""

    def __init__(self, *args: int) -> None:
        self._coordinates = np.array(args)    

    def __getitem__(self, key: int) -> int:
        return self._coordinates[key]

    def __sum__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(*(self._coordinates + other._coordinates))

    def __sub__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(*(self._coordinates - other._coordinates))

    def __eq__(self, other: 'Coordinate') -> bool:
        return np.array_equal(self._coordinates, other._coordinates)

    def __hash__(self) -> int:
        return hash(self._coordinates.tostring())

    def __repr__(self) -> str:
        return f'Coordinate({self._coordinates})'

    def __str__(self) -> str:
        return f'Coordinate({self._coordinates})'

    def __iter__(self) -> Iterator[int]:
        return iter(self._coordinates)

    def __len__(self) -> int:
        return len(self._coordinates)
