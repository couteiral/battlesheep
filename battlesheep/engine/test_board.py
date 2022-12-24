"""Tests for Board class."""

import numpy as np

from board import Board


def test_init():
    board = Board(8)
    assert board.get_size() == 8
    assert board.get_state().shape == (8, 8, 2)
    assert board.get_state().dtype == np.int8
    assert board.get_state().sum() == 0
    assert board.get_score(1) == 0

    holes = [(0, 0), (1, 1), (2, 2)]
    board = Board(8, holes=holes)
    assert board.get_size() == 8
    assert board.get_state().shape == (8, 8, 2)
    assert board.get_state().dtype == np.int8
    assert board.get_state().sum() == -3
    assert board.get_score(1) == 0

def test_actions():
    holes = [(1, 1), (2, 2), (0, 7)]
    board = Board(8, holes=holes)

    x1, y1 = (0, 0)
    x2, y2 = (7, 7)
    board.initialize_player(1, x1, y1, 16)
    board.initialize_player(2, x2, y2, 16)
    assert set(board.get_actions(1)) == {
        ((0, 0), 'R'),
        ((0, 0), 'DR'),
    }
    assert set(board.get_actions(2)) == {
        ((7, 7), 'UL'),
        ((7, 7), 'L'),
    }

    board.move_player(1, 0, 0, 2, 'R')
    board.move_player(2, 7, 7, 2, 'L')
    assert set(board.get_actions(1)) == {
        ((0, 0), 'R'),
        ((0, 0), 'DR'),
        ((0, 6), 'L'),
        ((0, 6), 'DL'),
        ((0, 6), 'DR')
    }
    assert set(board.get_actions(2)) == {
        ((7, 7), 'UL'),
        ((7, 7), 'L'),
        ((7, 0), 'R'),
        ((7, 0), 'UR'),
        ((7, 0), 'UL')
    }
