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
    assert square_grid.is_hole(*square_grid.to_cube(0, 0))
    assert square_grid.is_hole(*square_grid.to_cube(1, 1))
    assert square_grid.is_hole(*square_grid.to_cube(2, 2))

    q1, r1, s1 = square_grid.to_cube(1, 0)
    q2, r2, s2 = square_grid.to_cube(5, 7)
    square_grid.initialize_player(1, q1, r1, s1, 16)
    square_grid.initialize_player(2, q2, r2, s2, 16)
    assert not square_grid.is_empty(q1, r1, s1)
    assert not square_grid.is_empty(q2, r2, s2)
    assert not square_grid.is_hole(q1, r1, s1)
    assert not square_grid.is_hole(q2, r2, s2)
    assert square_grid.is_occupied(q1, r1, s1) 
    assert square_grid.is_occupied(q2, r2, s2)
    assert square_grid.is_occupied_by_player(q1, r1, s1, 1)
    assert square_grid.is_occupied_by_player(q2, r2, s2, 2)
    assert not square_grid.is_occupied_by_player(q1, r1, s1, 2)
    assert not square_grid.is_occupied_by_player(q2, r2, s2, 1)
    assert square_grid.units_at(q1, r1, s1) == 16
    assert square_grid.units_at(q2, r2, s2) == 16
    assert square_grid.get_score(1) == 1
    assert square_grid.get_score(2) == 1


def test_next_cell_search1():
    square_grid = HexagonalGrid(8)
    x1, y1 = 0, 0
    q1, r1, s1 = square_grid.to_cube(x1, y1)
    q2, r2, s2 = square_grid.get_next_moveable_cell(q1, r1, s1, 'R')
    x2, y2 = square_grid.to_offset(q2, r2, s2)
    assert x2 == 0 and y2 == 7
    assert square_grid.is_empty(q2, r2, s2)

    q2, r2, s2 = square_grid.get_next_moveable_cell(q1, r1, s1, 'L')
    x2, y2 = square_grid.to_offset(q2, r2, s2)
    assert x2 == x1 and y2 == y1
    assert square_grid.is_empty(q2, r2, s2)

def test_next_cell_search2():
    square_grid = HexagonalGrid(8, holes=[(0, 4)])
    x1, y1 = 0, 0
    q1, r1, s1 = square_grid.to_cube(x1, y1)
    q2, r2, s2 = square_grid.get_next_moveable_cell(q1, r1, s1, 'R')
    x2, y2 = square_grid.to_offset(q2, r2, s2)
    assert x2 == 0 and y2 == 3

def test_movement():
    square_grid = HexagonalGrid(8)
    x1, y1 = 0, 0
    q1, r1, s1 = square_grid.to_cube(x1, y1)
    square_grid.initialize_player(1, q1, r1, s1, 16)
    q2, r2, s2 = square_grid.get_next_moveable_cell(q1, r1, s1, 'R')
    assert square_grid.is_empty(q2, r2, s2)

    square_grid.move_player(1, x1, y1, 6, 'R')
    assert not square_grid.is_empty(q2, r2, s2)
    assert square_grid.units_at(q1, r1, s1) == 10
    assert square_grid.units_at(q2, r2, s2) == 6
    assert square_grid.player_at(q2, r2, s2) == 1