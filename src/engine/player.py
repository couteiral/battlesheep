"""Abstract base class for players."""

import abc
import random


class Player(abc.ABCMeta):
    """Abstract base class for players."""

    def calculate_move(self, state, actions):
        """Calculates the move to make."""
        raise NotImplementedError


class RandomPlayer(Player):
    """Naive player that makes random moves."""

    def calculate_move(self, state, actions):
        """Calculates the move to make."""
        return random.choice(actions)
