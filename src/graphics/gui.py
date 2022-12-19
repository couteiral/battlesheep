"""Functions to plot the board."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

import sys; sys.path.append('../engine/')
from board import Board


player_colors = {
    1: 'red',
    2: 'blue',
    3: 'green',
    4: 'yellow'
}


class BoardGUI:

    def __init__(self, board_size: int) -> None:
        self._board_size = board_size

        self._fig, self._ax = plt.subplots()
        self._ax.set_aspect('equal')
        self._ax.set_xlim(-1, board_size + 1)
        self._ax.set_ylim(-1, board_size + 1)
        self._ax.axis('off')
        plt.draw()

    def draw_board(self, board: Board) -> plt.Axes:
        """Draw the board."""
        assert board.get_size() == self._board_size
        for x in np.arange(self._board_size):
            for y in np.arange(self._board_size):

                if board.is_hole(x, y):
                    color = 'w'
                    edgecolor = 'w'
                elif board.is_empty(x, y):
                    color = 'gray'
                    edgecolor = 'k'
                else:
                    color = player_colors[board.player_at(x, y)]
                    edgecolor = 'k'

                if y % 2 != 0:
                    x_ = x
                else:
                    x_ = x + .5

                hex = RegularPolygon((x_, y), numVertices=6, radius=.5, 
                                    orientation=np.radians(120), 
                                    facecolor=color, alpha=0.2, edgecolor=edgecolor)
                self._ax.add_patch(hex)

                if not board.is_empty(x, y) and not board.is_hole(x, y):
                    self._ax.text(x_, y, board.units_at(x, y), ha='center', va='center', color='k')
        plt.draw()
                    