import enum


class Side(enum.Enum):
    """
    The four possible sides of a tile.
    """

    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


class Tile:

    def __init__(self):
        # TODO
        pass

    def rotate_clockwise(self):
        # TODO
        pass

    def rotate_counterclockwise(self):
        # TODO
        pass

    def __str__(self) -> str:
        # TODO
        pass
