"""Main game engine."""

from typing import Iterator, List

import numpy as np

from .player import Player
from .board import Board, Action, Coordinate
from ..graphics.gui import BoardGUI


class GameEnvironment:

    def __init__(self, size: int, players: List[Player],
    init_dict: dict, holes: Iterator[Coordinate], gui: bool = False) -> None:
        self._board = Board(size, holes)
        self._n_players = len(players)
        self.players = players
        self._init_dict = init_dict

        self._initialised = False
        self._gui = BoardGUI(self._board) if gui else None

    def _initialise(self):
        """Initialises the game."""
        for player_id, (c, n_units) in self._init_dict.items():
            self._board.initialize_player(player_id, c, n_units)
        self._initialised = True

    def _get_state(self) -> np.ndarray:
        """Returns the state of the board."""
        return self._board.get_state()

    def _get_actions(self, player_id: int) -> List[Action]:
        """Returns a list of the actions
        available to the player."""
        return self._board.get_actions(player_id)

    def _get_scores(self, player_id: int) -> int:
        """Returns the scores of each player."""
        return {player_id: self._board.get_score(player_id)
            for player_id in range(self._n_players)}

    def _make_move(self, player_id: int, x: int, y:int, direction: str) -> None:
        """Makes a move for the given player."""
        self._board.move_player(player_id, x, y, direction)

    def play_turn(self):
        """Plays a round of turns by all players."""
        if not self._initialised:
            self._initialise()

        for player_id, player in enumerate(self.players):
            state = self._get_state()
            actions = self._get_actions(player_id)
            move = player.get_move(state, actions)
            self._make_move(player, *move)

            if self._gui:
                self._gui.update_view(self._board)

    def play_game(self):
        """Plays a game."""
        while not self._finished():
            self.play_turn()
        return self._get_scores()
