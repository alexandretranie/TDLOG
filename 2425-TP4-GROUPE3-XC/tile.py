import dataclasses
import enum
import player
import utils

from dataclasses import dataclass, field
from typing import List, Optional, FrozenSet, Dict
from utils import Coords

"""
This module defines the tiles the player will place on the board.
"""


class Side(enum.Enum):
    """
    The four possible sides of a tile.
    """

    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


SIDE_NEXT_CLOCKWISE = {
    Side.NORTH: Side.EAST,
    Side.EAST: Side.SOUTH,
    Side.SOUTH: Side.WEST,
    Side.WEST: Side.NORTH,
}

SIDE_NEXT_COUNTERCLOCKWISE = {
    Side.NORTH: Side.WEST,
    Side.EAST: Side.NORTH,
    Side.SOUTH: Side.EAST,
    Side.WEST: Side.SOUTH,
}


@dataclasses.dataclass(frozen=True)
class Link:
    """
    A link is a road segment joining two sides (represented as a frozenset) of a
    tile, with the associated player color.
    """

    sides: frozenset[Side]
    color: player.Color

    def __str__(self):
        first_side, second_side = list(self.sides)
        return f"{first_side.value}-{second_side.value}:{self.color.value}"


TILE_HEIGHT = 5
TILE_WIDTH = 9
# fmt: off
EMPTY_TILE = [
    "+---#---+",
    "|       |",
    "#       #",
    "|       |",
    "+---#---+",
]


# The description of where to put the various components of a link, as a
# dictionary whose keys are the frozensets containing the sides part of the
# link. The associated values are tuples whose components are:
# - the row of the color;
# - the column of the color;
# - a list of triples indicating the starting rows, starting columns and texts to
#   insert to represent the road segments.
LINK_POSITIONS = {
    frozenset({Side.NORTH, Side.WEST}): (2, 2, [(1, 1, "####"), (2, 1, "#")]),
    frozenset({Side.NORTH, Side.EAST}): (2, 6, [(1, 4, "####"), (2, 7, "#")]),
    frozenset({Side.SOUTH, Side.WEST}): (2, 2, [(3, 1, "####"), (2, 1, "#")]),
    frozenset({Side.SOUTH, Side.EAST}): (2, 6, [(3, 4, "####"), (2, 7, "#")]),
    frozenset({Side.NORTH, Side.SOUTH}): (2, 4, [(1, 4, "#"), (3, 4, "#")]),
    frozenset({Side.WEST, Side.EAST}): (2, 4, [(2, 1, "###"), (2, 5, "###")]),
}
# fmt: on


class Tile:
    """
    A tile is simply a list of links.
    """
    links: List[Link] = field(default_factory=list)

    def get_link(self, side: Side) -> Optional[Link]:
        """Retourne le lien connecté au côté spécifié, s'il existe."""
        for link in self.links:
            if side in link.sides:
                return link
        return None

    def __init__(self, links):
        assert len(links) <= 2, "invalid links"
        assert all(map(lambda link: len(link.sides) == 2, links)), "invalid links"
        assert (
            len(links) < 2 or len(links[0].sides.union(links[1].sides)) == 4
        ), "invalid links"
        self._links = links

    @property
    def links(self):
        return self._links

    def _rotate_link(self, link, side_dict):
        """
        Rotate the passed link by mapping each of its sides using `side_dict`.
        """
        return Link(
            sides=frozenset({side_dict[side] for side in link.sides}), color=link.color
        )

    def _rotate(self, side_dict):
        """
        Rotate all the links of the tile, mapping each of their sides using `side_dict`.
        """
        self._links = [self._rotate_link(link, side_dict) for link in self._links]

    def rotate_clockwise(self):
        self._rotate(SIDE_NEXT_CLOCKWISE)

    def rotate_counterclockwise(self):
        self._rotate(SIDE_NEXT_COUNTERCLOCKWISE)

    def __str__(self):
        first_side, second_side = list(self.sides)
        return f"{first_side.value}-{second_side.value}:{self.color}"

    def display_in_chars(self, chars, start_row, start_column):
        """
        Put the representation of the tile into the passed `chars` (list of
        list of characters), using `start_row` and `start_column` as the
        coordinates of the top left corner of the tile.
        """
        utils.set_2d_texts(chars, start_row, start_column, EMPTY_TILE)
        for link in self._links:
            color_row_delta, color_column_delta, road_segments = LINK_POSITIONS[
                link.sides
            ]
            utils.set_2d_text(
                chars,
                start_row + color_row_delta,
                start_column + color_column_delta,
                player.COLOR_LETTER[link.color],
            )
            for row_delta, column_delta, text in road_segments:
                utils.set_2d_text(
                    chars, start_row + row_delta, start_column + column_delta, text
                )
    def get_adjacent_positions(self) -> List[Coords]:
        """
        Retourne une liste de positions vides qui sont adjacentes à une tuile déjà placée.
        """
        adjacent_positions = set()

        # Parcourir toutes les tuiles placées et trouver les positions adjacentes
        for row in range(self._height):
            for col in range(self._width):
                if self._tiles[row][col] is not None:  # Il y a une tuile ici
                    # Vérifier les 4 directions autour
                    for delta_row, delta_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        adj_row = row + delta_row
                        adj_col = col + delta_col
                        if 0 <= adj_row < self._height and 0 <= adj_col < self._width:
                            if self._tiles[adj_row][adj_col] is None:  # Position vide adjacente
                                adjacent_positions.add(Coords(adj_row, adj_col))

        return list(adjacent_positions)

    def generate_possible_moves(self, tile: 'Tile') -> List['Move']:
        """
        Génère tous les coups possibles pour une tuile donnée (positions adjacentes + rotations).
        """
        possible_moves = []
        # Récupérer les positions adjacentes où on peut placer une tuile
        adjacent_positions = self.get_adjacent_positions()

        # Pour chaque position adjacente, générer les 4 rotations possibles
        for position in adjacent_positions:
            for rotation in [0, 90, 180, 270]:
                possible_moves.append(Move(position=position, rotation=rotation))

        return possible_moves

    def place_tile_with_rotation(self, coords: 'Coords', tile: 'Tile', rotation: int):
        """
        Place une tuile sur le plateau avec la rotation spécifiée.
        """
        rotated_tile = self.rotate_tile(tile, rotation)
        self._tiles[coords.row][coords.column] = rotated_tile

    def rotate_tile(self, tile: 'Tile', rotation: int) -> 'Tile':
        """
        Retourne une nouvelle tuile avec la rotation spécifiée (0, 90, 180, 270 degrés).
        """
        rotated_tile = Tile(links=tile.links[:])  # Créer une copie de la tuile
        for _ in range(rotation // 90):
            rotated_tile.rotate_clockwise()
        return rotated_tile