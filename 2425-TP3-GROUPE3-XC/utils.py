def make_2d_chars(height, width, value):
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
    column = start_column
    for char in text:
        chars[row][column] = char
        column += 1


def set_2d_texts(
    chars,
    start_row,
    start_column,
    texts,
):
    row = start_row
    for text in texts:
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
    for row in range(start_row, start_row + height):
        for column in range(start_column, start_column + width):
            chars[row][column] = value
