"""Tests for the tiling utilities."""

import numpy as np

from tiling import SingleHexagon, BasicTile, HexCoord

def test_hexagon_join():

    hexagon1 = SingleHexagon()
    hexagon2 = SingleHexagon()
    hexagon1.join(hexagon2, HexCoord(0, 0, 0), HexCoord(0, 0, 0), 'R')
    assert set(hexagon1.space_occupied) == {
        HexCoord( 0,  0,  0),
        HexCoord( 1,  0, -1),
    }

def test_hexagons_to_tile():

    hexagon1 = SingleHexagon()
    hexagon2 = SingleHexagon()
    hexagon3 = SingleHexagon()
    hexagon4 = SingleHexagon()
    hexagon1.join(hexagon2, HexCoord(0, 0, 0), HexCoord(0, 0, 0), 'R')
    hexagon1.join(hexagon3, HexCoord(0, 0, 0), HexCoord(0, 0, 0), 'UL')
    hexagon1.join(hexagon4, HexCoord(0, 0, 0), HexCoord(0, 0, 0), 'UR')

    ref = BasicTile()
    assert set(hexagon1.space_occupied) == set(ref.space_occupied)

def test_tile_join():

    tile1 = BasicTile()
    tile2 = BasicTile()
    tile1.join(tile2, HexCoord(1, -1, 0), HexCoord(0, 0, 0), 'UR')

    assert set(tile1.space_occupied) == {
        HexCoord( 0,  0,  0),
        HexCoord( 0, -1,  1),
        HexCoord( 1, -1,  0),
        HexCoord( 1,  0, -1),
        HexCoord( 2, -2,  0),
        HexCoord( 2, -3,  1),
        HexCoord( 3, -3,  0),
        HexCoord( 3, -2, -1),
    }
