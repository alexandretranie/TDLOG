import player
import tile


"""
This module provides utility functions to build the default deck, or load a
deck from a file.

The specification of the format for such files is as follows:

- the format is *line-oriented*, which means that each line is interpreted
  independently;
- the `%` character marks the start of a comment, which ends at the end of the
  line;
- the comments are ignored;
- the lines with only space characters are ignored (this includes the lines
  starting with one or several space characters and ending with a comment);
- there are 3 kinds of *useful* lines, introduced by one of the following
  directives: `NO_LINKS`, `ONE_LINK` and `TWO_LINKS`;
- the `NO_LINKS` directive appears alone on the line (ignoring spaces and
  comments), and represents a tile with no links;
- the `ONE_LINK` directive is followed by a single link specification (ignoring
  spaces and comments), and represents a tile with one link;
- the `TWO_LINKS` directive is followed by a first link specification, the `&`
  character, and a second link specification (ignoring spaces and comments), and
  represents a tile with two links;
- a link specification has the following form: *side* `-` *side* `:` *color*,
  where the possible values for the sides are `north`, `east`, `south`, `west`,
  and the possible values for the color are `blue`, `purple`, `red`, `yellow`.
"""


def tile_no_links():
    """
    Create a tile with no links.
    """
    return tile.Tile(links=[])


def tile_one_link(sides, color):
    """
    Create a tile with one link whose sides are passed as a tuple, and a player color.
    """
    assert len(sides) == 2 and sides[0] != sides[1], "invalid sides"
    return tile.Tile(
        links=[
            tile.Link(
                sides=frozenset(sides),
                color=color,
            )
        ]
    )


def tile_two_links(
    sides1,
    color1,
    sides2,
    color2,
):
    """
    Create a tile with two links whose sides are passed as tuples, and player colors.
    """
    assert len(sides1) == 2 and sides1[0] != sides1[1], "invalid sides1"
    assert len(sides2) == 2 and sides2[0] != sides2[1], "invalid sides2"
    assert len(set(sides1 + sides2)) == 4
    assert color1 != color2, "invalid colors"
    return tile.Tile(
        links=[
            tile.Link(
                sides=frozenset(sides1),
                color=color1,
            ),
            tile.Link(
                sides=frozenset(sides2),
                color=color2,
            ),
        ]
    )


def tile_consecutive(color):
    """
    Create a tile with one link between consecutive sides.
    """
    return tile_one_link((tile.Side.NORTH, tile.Side.EAST), color)


def tile_opposite(color):
    """
    Create a tile with one link between opposite sides.
    """
    return tile_one_link((tile.Side.NORTH, tile.Side.SOUTH), color)


def tile_consecutives(color1, color2):
    """
    Create a tile with two links between consecutive sides.
    """
    assert color1 != color2, "invalid colors"
    return tile_two_links(
        (tile.Side.NORTH, tile.Side.EAST),
        color1,
        (tile.Side.SOUTH, tile.Side.WEST),
        color2,
    )


def make_tiles():
    """
    Return the list of all the tiles part of the game, i.e. the default deck.
    """
    return (
        [
            # 4 tiles with no links
            tile_no_links()
            for _ in range(4)
        ]
        + [
            # 8 tiles (2 per color) with one link between consecutive sides
            tile_consecutive(color)
            for color in player.Color
            for _ in range(2)
        ]
        + [
            # 12 tiles (3 per color) with one link between opposite sides
            tile_opposite(color)
            for color in player.Color
            for _ in range(3)
        ]
        + [
            # 12 tiles (2 per combination of two different colors)
            # with two links between consecutive sides
            tile_consecutives(color1, color2)
            for color1 in player.Color
            for color2 in player.Color
            if color1.value < color2.value
            for _ in range(2)
        ]
    )


class InvalidFormat(Exception):
    """
    The exception to be raised if a file does not follow the deck specification.
    """

    def __init__(self, line_num, message):
        super().__init__()
        assert line_num > 0, "invalid line_num"
        self._line_num = line_num
        self._message = message

    @property
    def line_num(self):
        return self._line_num

    @property
    def message(self):
        return self._message

    def __str__(self):
        return f"line {self._line_num}: {self._message}"


def decode_color(line_num, text):
    """
    Decode the passed text (`str` value) into a player color, raising
    `InvalidFormat` if the value does not represent a color.
    """
    try:
        return player.Color(text.strip())
    except ValueError:
        raise InvalidFormat(line_num, f"invalid color ({text})")


def decode_side(line_num, text):
    """
    Decode the passed text (`str` value) into a side, raising `InvalidFormat`
    if the value does not represent a side.
    """
    try:
        return tile.Side(text.strip())
    except ValueError:
        raise InvalidFormat(line_num, f"invalid side ({text})")


def decode_sides(line_num, text):
    """
    Decode the passed text (`str` value) into a couple of sides, raising
    `InvalidFormat` if the value does not represent two sides separated by a
    dash character.
    """
    sides = text.split("-")
    if len(sides) != 2:
        raise InvalidFormat(
            line_num, "a link should have two sides separated by a dash"
        )
    side0 = decode_side(line_num, sides[0])
    side1 = decode_side(line_num, sides[1])
    if side0 == side1:
        raise InvalidFormat(line_num, "a link should be between two different sides")
    return side0, side1


def decode_link(line_num, text):
    """
    Decode the passed text (`str` value) into a link, represented as a couple
    whose components are a couple of side and a color. Raises `InvalidFormat`
    if the value does not represent a link.
    """
    parts = text.split(":")
    if len(parts) != 2:
        raise InvalidFormat(
            line_num, "a link should have two sides and a color separated by a colon"
        )
    return decode_sides(line_num, parts[0]), decode_color(line_num, parts[1])


def decode_line(line_num, text):
    """
    Decode the passed text (`str` value) into a `Tile` instance, raising
    `InvalidFormat` if the line does not follow the format above.
    """
    items = text.split(" ", maxsplit=1)
    match items[0]:
        case "NO_LINKS":
            if len(items) != 1:
                raise InvalidFormat(
                    line_num, "a NO_LINKS should not be followed by anything"
                )
            return tile_no_links()
        case "ONE_LINK":
            if len(items) != 2:
                raise InvalidFormat(
                    line_num, "a ONE_LINK should be followed by a link definition"
                )
            sides, color = decode_link(line_num, items[1])
            return tile_one_link(sides, color)
        case "TWO_LINKS":
            if len(items) != 2:
                raise InvalidFormat(
                    line_num, "a TWO_LINKS should be followed by link definitions"
                )
            links = items[1].split("&")
            if len(links) != 2:
                raise InvalidFormat(
                    line_num, "a TWO_LINKS should be followed by 2 link definitions"
                )
            sides1, color1 = decode_link(line_num, links[0])
            sides2, color2 = decode_link(line_num, links[1])
            if len(set(sides1 + sides2)) != 4:
                raise InvalidFormat(line_num, "links should not have overlapping sides")
            if color1 == color2:
                raise InvalidFormat(line_num, "links should have different colors")
            return tile_two_links(sides1, color1, sides2, color2)
        case _:
            raise InvalidFormat(line_num, f"unknown directive {items[0]}")


COMMENT_SIGN = "%"


def load_tiles(path):
    """
    Load the deck from the file whose path is passed. Raises `InvalidFormat` if
    the file does not follow the specifiation above or contains no tiles, and
    raises `IOError` if any i/o error happens.
    """
    with open(path, "r") as file:
        lines = file.readlines()
    tiles = []
    for line_num, line in enumerate(lines, start=1):
        line_without_comment = line.split(COMMENT_SIGN)[0].strip()
        if len(line_without_comment) > 0:
            tiles.append(decode_line(line_num, line_without_comment))
    if len(tiles) > 0:
        return tiles
    else:
        raise InvalidFormat(0, "empty deck")
