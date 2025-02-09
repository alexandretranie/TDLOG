"""
This module defines utility functions to manipulate rectangles of characters
values as list of list of strings, typically used to make structured printing
easier.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Coords:
    row: int
    column: int

    def __str__(self):
        return f"Coords(row={self.row}, column={self.column})"
    
    def __hash__(self):
        return hash((self.row, self.column))

    def __eq__(self, other):
        if isinstance(other, Coords):
            return self.row == other.row and self.column == other.column
        return False


def make_2d_chars(height, width, value):
    """
    Returns a (rectangular) list of lists of character values (as strings of
    length 1). The returned value has `height` lists and each list has `width`
    values, all equal to `value`.
    """
    assert height >= 0, "invalid height"
    assert width >= 0, "invalid width"
    assert len(value) == 1, "invalid value"
    lines = []
    for _ in range(height):
        lines.append([value] * width)
    return lines


def set_2d_text(
    chars,
    row,
    start_column,
    text,
):
    """
    Set values of the list of lists of characters `chars` to the individual
    characters of the string `text`. Characters are set horizontally, on the
    passed `row`, from `start_column` and then from left to right.
    """
    assert 0 <= row < len(chars), "invalid row"
    column = start_column
    for char in text:
        assert 0 <= start_column < len(chars[row]), "invalid start_column"
        assert 0 <= start_column + len(text) <= len(chars[row]), "invalid start_column"
        chars[row][column] = char
        column += 1


def set_2d_texts(
    chars,
    start_row,
    start_column,
    texts,
):
    """
    Set values of the list of lists of characters `chars` to the individual
    of the strings from the `texts` list, by repeatedly calling `set_2d_text`
    on each string of `texts`, using the same starting column and an
    increasing value for the row.
    """
    assert 0 <= start_row < len(chars), "invalid start_row"
    assert 0 <= start_row + len(texts) <= len(chars), "invalid start_row"
    row = start_row
    for text in texts:
        assert 0 <= start_row < len(chars[row]), "invalid start_row"
        assert 0 <= start_row + len(text) <= len(chars[row]), "invalid start_row"
        set_2d_text(chars, row, start_column, text)
        row += 1


def fill_2d_chars(
    chars,
    start_row,
    height,
    start_column,
    width,
    value,
):
    """
    Set all the values in a sub-rectangle of `chars` (list of list of
    characters) to `value`. The top left coordinates of the sub-rectangle is
    given by `start_row` and `start_column`, and its dimensions are given by
    `height` and `width`.
    """
    assert 0 <= start_row < len(chars), "invalid start_row"
    assert 0 <= start_row + height <= len(chars), "invalid start_row"
    assert len(value) == 1, "invalid value"
    for row in range(start_row, start_row + height):
        assert 0 <= start_column < len(chars[row]), "invalid start_column"
        assert 0 <= start_column + width <= len(chars[row]), "invalid start_column"
        for column in range(start_column, start_column + width):
            chars[row][column] = value
