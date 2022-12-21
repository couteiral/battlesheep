"""Functions to plot the board."""

from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from .board import Board


player_colors = {
    1: 'red',
    2: 'blue',
    3: 'green',
    4: 'yellow'
}

class BoardGUI:

    def __init__(self, board: Board) -> None:
        self.board_size = board.get_size()
        self.fig, self.ax = self._init_canvas(board.get_size())
        self._draw_board(board)

    def _init_canvas(self, board_size: int) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_xlim(-1, board_size)
        ax.set_ylim(-1, board_size)
        ax.axis('off')
        ax.invert_yaxis()
        return fig, ax

    def _draw_board(self, board: Board) -> None:
        """Draw the board for the first time."""

        self._board, self._labels = [], []
        for x in np.arange(self.board_size):
            for y in np.arange(self.board_size):

                if board.is_hole(x, y):
                    color = 'w'
                    edgecolor = 'w'
                elif board.is_empty(x, y):
                    color = 'gray'
                    edgecolor = 'k'

                if y % 2 != 0:
                    x_ = x
                else:
                    x_ = x + .5

                hex = RegularPolygon((x_, y), numVertices=6, radius=.5, 
                                    orientation=np.radians(120), 
                                    facecolor=color, alpha=0.2, edgecolor=edgecolor)
                text = self.ax.text(x_, y, '', ha='center', va='center', color='k')
                self._board.append(hex)
                self._labels.append(text)
                self.ax.add_patch(hex)

    def update_view(self, board: Board) -> None:
        """Update the view of the board."""

        for x in np.arange(self.board_size):
            for y in np.arange(self.board_size):
                if not board.is_empty(x, y) and not board.is_hole(x, y):
                    player = board.player_at(x, y)
                    color = player_colors[player]
                    self._board[x + y * self.board_size].set_facecolor(color)
                    self._labels[x + y * self.board_size].set_text(board.units_at(x, y))