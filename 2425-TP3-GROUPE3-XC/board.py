import dataclasses
import tile
import utils


@dataclasses.dataclass
class Coords:

    row: int
    column: int

    def __str__(self):
        return f"{self.row}, {self.column}"


EMPTY_SPACE = "."


class Board:

    def __init__(self):
        self._height = 1
        self._width = 1
        self._tiles = [[None]]

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def __getitem__(self, key):
        return self._tiles[key.row][key.column]

    def __setitem__(self, key, value):
        self._tiles[key.row][key.column] = value
        if key.row == self._height - 1:
            self._tiles.append([None] * self._width)
            self._height += 1
        if key.row == 0:
            self._tiles.insert(0, [None] * self._width)
            self._height += 1
        if key.column == self._width - 1:
            for row_tiles in self._tiles:
                row_tiles.append(None)
            self._width += 1
        if key.column == 0:
            for row_tiles in self._tiles:
                row_tiles.insert(0, None)
            self._width += 1

    def display(self):
        chars = utils.make_2d_chars(
            height=self._height * tile.TILE_HEIGHT,
            width=self._width * tile.TILE_WIDTH,
            value=EMPTY_SPACE,
        )
        for row in range(self._height):
            for column in range(self._width):
                coords = Coords(row=row, column=column)
                cell = self[coords]
                if cell is not None:
                    cell.display_in_chars(
                        chars,
                        start_row=row * tile.TILE_HEIGHT,
                        start_column=column * tile.TILE_WIDTH,
                    )
        print("\n".join(map(lambda x: "".join(x), chars)))
