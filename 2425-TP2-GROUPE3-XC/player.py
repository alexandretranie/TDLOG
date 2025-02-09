import enum


class Color(enum.Enum):
    """
    The possible colors of a player.
    """

    BLUE = "blue"
    PURPLE = "purple"
    RED = "red"
    YELLOW = "yellow"


COLOR_LETTER = {
    Color.BLUE: "B",
    Color.PURPLE: "P",
    Color.RED: "R",
    Color.YELLOW: "Y",
}


class Player:
    def __init__(self):
        # TODO
        pass
