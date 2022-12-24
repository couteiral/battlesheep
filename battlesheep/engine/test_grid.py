"""Tests for HexagonalGrid class."""

import numpy as np

from grid import HexagonalGrid


def test_init():
    square_grid = HexagonalGrid(8)
    assert square_grid.get_size() == 8
    assert square_grid.get_state().shape == (8, 8, 2)
    assert square_grid.get_state().dtype == np.int8
    assert square_grid.get_state().sum() == 0
    assert square_grid.get_score(1) == 0

    holes = [(0, 0), (1, 1), (2, 2)]
    square_grid = HexagonalGrid(8, holes=holes)
    assert square_grid.get_size() == 8
    assert square_grid.get_state().shape == (8, 8, 2)
    assert square_grid.get_state().dtype == np.int8
    assert square_grid.get_state().sum() == -3
    assert square_grid.get_score(1) == 0

def test_coordinate_conversion():
    square_grid = HexagonalGrid(8)
    for q in range(-4, 4):
        for r in range(-4, 4):
            for s in range(-4, 4):
                if q + r + s == 0:
                    x, y = square_grid.to_offset(q, r, s)
                    assert x >= 0 and x < 8
                    assert y >= 0 and y < 8
                    q_, r_, s_ = square_grid.to_cube(x, y)
                    assert q == q_
                    assert r == r_
                    assert s == s_

def test_coordinate_conversion2():
    square_grid = HexagonalGrid(8)
    for x in range(8):
        for y in range(8):
            q, r, s = square_grid.to_cube(x, y)
            x_, y_ = square_grid.to_offset(q, r, s)
            assert x == x_
            assert y == y_


def test_grid_values():
    holes = [(0, 0), (1, 1), (2, 2)]
    square_grid = HexagonalGrid(8, holes=holes)
    assert square_grid.is_hole(0, 0)
    assert square_grid.is_hole(1, 1)
    assert square_grid.is_hole(2, 2)

    x1, y1 = (1, 0)
    x2, y2 = (5, 7)
    square_grid.initialize_player(1, x1, y1, 16)
    square_grid.initialize_player(2, x2, y2, 16)
    assert not square_grid.is_empty(x1, y1)
    assert not square_grid.is_empty(x2, y2)
    assert not square_grid.is_hole(x1, y1)
    assert not square_grid.is_hole(x2, y2)
    assert square_grid.is_occupied(x1, y1) 
    assert square_grid.is_occupied(x2, y2)
    assert square_grid.is_occupied_by_player(x1, y1, 1)
    assert square_grid.is_occupied_by_player(x2, y2, 2)
    assert not square_grid.is_occupied_by_player(x1, y1, 2)
    assert not square_grid.is_occupied_by_player(x2, y2, 1)
    assert square_grid.units_at(x1, y1) == 16
    assert square_grid.units_at(x2, y2) == 16
    assert square_grid.get_score(1) == 1
    assert square_grid.get_score(2) == 1


def test_next_cell_search1():
    square_grid = HexagonalGrid(8)
    x1, y1 = (0, 0)
    x2, y2 = square_grid.get_next_moveable_cell(x1, y1, 'R')
    assert x2 == 0 and y2 == 7
    assert square_grid.is_empty(x2, y2)

    x2, y2 = square_grid.get_next_moveable_cell(x1, y1, 'L')
    assert x2 == x1 and y2 == y1
    assert square_grid.is_empty(x2, y2)

def test_next_cell_search2():
    square_grid = HexagonalGrid(8, holes=[(0, 4)])
    x1, y1 = (0, 0)
    x2, y2 = square_grid.get_next_moveable_cell(x1, y1, 'R')
    assert x2 == 0 and y2 == 3

def test_movement():
    square_grid = HexagonalGrid(8)
    x1, y1 = (0, 0)
    square_grid.initialize_player(1, x1, y1, 16)
    x2, y2 = square_grid.get_next_moveable_cell(x1, y1, 'R')
    assert square_grid.is_empty(x2, y2)

    square_grid.move_player(1, x1, y1, 6, 'R')
    assert not square_grid.is_empty(x2, y2)
    assert square_grid.units_at(x1, y1) == 10
    assert square_grid.units_at(x2, y2) == 6
    assert square_grid.player_at(x2, y2) == 1