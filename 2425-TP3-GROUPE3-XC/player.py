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

    def __init__(self, color, num_pawns):
        self._color = color
        self._num_pawns = num_pawns

    @property
    def color(self):
        return self._color

    @property
    def num_pawns(self):
        return self._num_pawns

    @num_pawns.setter
    def num_pawns(self, value):
        self._num_pawns = value


class HumanPlayer(Player):

    def __init__(self, color, num_pawns, name):
        super().__init__(color, num_pawns)
        self._name = name

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name


class RandomPlayer(Player):

    def __init__(self, color, num_pawns):
        super().__init__(color, num_pawns)

    def __str__(self):
        return "random"


class AILevel(enum.Enum):
    EASY = "easy"
    HARD = "hard"


class AIPlayer(Player):

    def __init__(self, color, num_pawns, level):
        super().__init__(color, num_pawns)
        self._level = level

    @property
    def level(self):
        return self._level

    def __str__(self):
        return f"AI ({self._level})"
