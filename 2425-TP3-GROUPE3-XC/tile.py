import dataclasses
import enum
import player
import utils


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
    Represente un lien entre deux côtes d'une tuile avec une couleur.
    Attributes:
        sides (frozenset[Side]): A set of two sides of a tile.
        color (player.Color): The color associated with the link.
    """
    sides: frozenset[Side]
    color: player.Color

    def __post_init__(self):
        # Validation: S'assure qu'il y a bien un lien entre les deux côtés.
        if len(self.sides) != 2:
            raise ValueError("A link must connect exactly two sides.")
        # Validation: S'assure que les deux côtés sont distincts. 
        if len(set(self.sides)) != 2:
            raise ValueError("The two sides in a link must be distinct.")
    def __str__(self):
        """
        Retourne une représentation string du lien
        """
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
# fmt: on
LINK_POSITIONS = {
    frozenset({Side.NORTH, Side.WEST}): (2, 2, [(1, 1, "####"), (2, 1, "#")]),
    frozenset({Side.NORTH, Side.EAST}): (2, 6, [(1, 4, "####"), (2, 7, "#")]),
    frozenset({Side.SOUTH, Side.WEST}): (2, 2, [(3, 1, "####"), (2, 1, "#")]),
    frozenset({Side.SOUTH, Side.EAST}): (2, 6, [(3, 4, "####"), (2, 7, "#")]),
    frozenset({Side.NORTH, Side.SOUTH}): (2, 4, [(1, 4, "#"), (3, 4, "#")]),
    frozenset({Side.WEST, Side.EAST}): (2, 4, [(2, 1, "###"), (2, 5, "###")]),
}


class Tile:

    def __init__(self, links):
        self._links = links

    @property
    def links(self):
        return self._links

    def _rotate_link(self, link, side_dict):
        return Link(
            sides=frozenset({side_dict[side] for side in link.sides}), color=link.color
        )

    def _rotate(self, side_dict):
        self._links = [self._rotate_link(link, side_dict) for link in self._links]

    def rotate_clockwise(self):
        self._rotate(SIDE_NEXT_CLOCKWISE)

    def rotate_counterclockwise(self):
        self._rotate(SIDE_NEXT_COUNTERCLOCKWISE)

    def __str__(self):
        if self._links:
            return " & ".join(map(str, self._links))
        else:
            return "no links"

    def display_in_chars(self, chars, start_row, start_column):
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

print(EMPTY_TILE)
