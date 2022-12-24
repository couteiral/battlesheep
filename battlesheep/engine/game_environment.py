"""Main game engine."""

from typing import Iterator, List

import numpy as np

from .player import Player
from .board import Board, Action, Coordinate
from ..graphics.gui import BoardGUI


class GameEnvironment:

    def __init__(self, size: int, players: List[Player],
    init_dict: dict, holes: Iterator[Coordinate], gui: bool = False) -> None:
        self.board = Board(size, holes)
        self.n_players = len(players)
        self.players = players
        self.init_dict = init_dict

        self._initialised = False
        self._gui = BoardGUI(self.board) if gui else None

    def _initialise(self):
        """Initialises the game."""
        for player_id, (x, y, n_units) in self.init_dict.items():
            self.board.initialize_player(player_id, x, y, n_units)
        if self._gui:
            self._gui.update_view(self.board)
        self._initialised = True

    def _get_state(self) -> np.ndarray:
        """Returns the state of the board."""
        return self.board.get_state()

    def _get_actions(self, player_id: int) -> List[Action]:
        """Returns a list of the actions
        available to the player."""
        assert player_id >= 1
        return [act for act in self.board.get_actions(player_id)]

    def _get_scores(self) -> dict:
        """Returns the scores of each player."""
        return {player_id: self.board.get_score(player_id)
            for player_id in range(1, self.n_players+1)}

    def _make_move(self, player_id: int, x: int, y: int, n_units: int, direction: str) -> None:
        """Makes a move for the given player."""
        assert player_id >= 1
        self.board.move_player(player_id, x, y, n_units, direction)

    def _finished(self):
        """Returns True if the game is finished."""
        return len(self._get_actions(1)) == 0

    def play_turn(self):
        """Plays a round of turns by all players."""
        if not self._initialised:
            self._initialise()

        for player_id in range(1, len(self.players)+1):
            player = self.players[player_id-1]
            state = self._get_state()
            actions = self._get_actions(player_id)
            (x, y), direction, n_units = player.calculate_move(state, actions)
            self._make_move(player_id, x, y, n_units, direction)
            if self._gui:
                self._gui.update_view(self.board)

    def play_game(self):
        """Plays a game."""
        if not self._initialised:
            self._initialise()
        while not self._finished():
            self.play_turn()
        return self._get_scores()
