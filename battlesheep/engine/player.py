"""Abstract base class for players."""

import random


class Player():
    """Abstract base class for players."""

    def calculate_move(self, state, actions):
        """Calculates the move to make."""
        raise NotImplementedError


class RandomPlayer(Player):
    """Naive player that makes random moves."""

    def calculate_move(self, state, actions):
        """Calculates the move to make."""
        (x, y), direction = random.choice(actions)
        max_units = state[x, y, 1]
        n_units = random.randint(1, max_units-1)
        return (x, y), direction, n_units
