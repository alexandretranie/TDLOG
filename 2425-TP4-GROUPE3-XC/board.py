import dataclasses
import enum
import player
import utils

from dataclasses import dataclass, field
from typing import List, Optional, FrozenSet, Dict
from tile import Side, Tile
from utils import Coords




@dataclass
class Move:
    position: Coords  # Position où placer la tuile
    rotation: int  # Rotation de la tuile (0°, 90°, 180°, 270°)

"""
This module defines a board, which is an extensible rectangle of tiles.
"""

class BoardException(Exception):
    """
    Exception to be raised when the board is inappropriately used, e.g.
    out-of-bounds accesses.
    """

    def __init__(self, message, coords):
        super().__init__()
        self._message = message
        self._coords = coords

    @property
    def message(self):
        return self._message

    @property
    def coords(self):
        return self._coords

    def __str__(self):
        return f"{self._message} ({self._coords})"


EMPTY_SPACE = "."


class Board:
    """
    Board, as an extensible rectangle of tiles, represented as a list of list
    of `Tile` instances; `None` is used to indicate a given cell is empty.
    """

    def __init__(self):
        """
        Create a 1x1 board, whose only cell is empty (this set to `None`).
        """
        self._height = 1
        self._width = 1
        self._tiles = [[None]]
        self._players: Dict[str, player.Player] = {}  # Dictionnaire des joueurs avec leur couleur


    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def _check_coords(self, coords):
        """
        Raise `BoardException` if the passed coordinates are invalid, doing notheing
        otherwise.
        """
        if not (0 <= coords.row < self._height and 0 <= coords.column < self._width):
            raise BoardException("invalid coordinates", coords)

    def __getitem__(self, key):
        """
        Read access to cell whose `Coords` are passed. Raises `BoardException`
        if the coordinates are invalid.
        """
        self._check_coords(key)
        return self._tiles[key.row][key.column]

    def __setitem__(self, key, value):
        """
        Write access to cell whose `Coords` are passed. Raises `BoardException`
        if the coordinates are invalid, or if there is already a tile at the
        coordinates.

        Ensures there is always room to place a tile next to all tiles in the
        board by automatically adding rows and columns as necessary. As a
        consequence, the coordinates of already-placed tiles may be changed.
        """
        self._check_coords(key)
        if self._tiles[key.row][key.column] is None:
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
        else:
            raise BoardException("tile already set", key)

    def display(self):
        """
        Print the board onto the standard output.
        """
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

    def add_player(self, new_player: player.Player):
        """Ajoute un joueur à la partie."""
        self._players[new_player.color] = new_player

    def get_adjacent_tile(self, coords: Coords, side: Side) -> Optional[Tile]:
        """Retourne la tuile adjacente dans la direction spécifiée."""
        row, column = coords.row, coords.column
        if side == Side.NORTH and row > 0:
            return self[Coords(row - 1, column)]
        elif side == Side.SOUTH and row < self._height - 1:
            return self[Coords(row + 1, column)]
        elif side == Side.WEST and column > 0:
            return self[Coords(row, column - 1)]
        elif side == Side.EAST and column < self._width - 1:
            return self[Coords(row, column + 1)]
        return None
    
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
                                new_coords = Coords(adj_row, adj_col)
                                print(f"Adding Coords to set: {new_coords.row}, {new_coords.column}")
                                adjacent_positions.add(new_coords)

        return list(adjacent_positions)
    
    def is_path_closed(self, coords: Coords, tile: Tile) -> bool:
        """Détermine si un chemin est clos."""
        closed_paths = True
        print(f"Vérification si le chemin est clos pour la tuile en {coords}")
        for link in tile.links:
            for side in link.sides:
                adjacent_tile = self.get_adjacent_tile(coords, side)
                if adjacent_tile:
                    opposite_side = {
                        Side.NORTH: Side.SOUTH,
                        Side.SOUTH: Side.NORTH,
                        Side.EAST: Side.WEST,
                        Side.WEST: Side.EAST,
                    }[side]

                    adjacent_link = adjacent_tile.get_link(opposite_side)
                    if not adjacent_link or adjacent_link.color != link.color:
                        closed_paths = False
                else:
                    closed_paths = False
        print(f"Chemin clos : {closed_paths}")
        return closed_paths

    def place_pawn_if_path_closed(self, coords: Coords, tile: Tile):
        """Place des pions si un chemin est clos après la pose d'une tuile."""
        if self.is_path_closed(coords, tile):
            for link in tile.links:
                player_instance = self._players.get(link.color)
                if player_instance and player_instance.num_pawns > 0:
                    print(f"Placing a pawn for player {player_instance.color} on a closed path.")
                    player_instance.num_pawns -= 1
                    print(f"Pions restants pour {player_instance.color}: {player_instance.num_pawns}")
                else:
                    print(f"Player {player_instance.color} has no pawns left.")
        else:
            print(f"Chemin non clos, aucun pion placé pour {tile}.")

    
    def place_tile_with_rotation(self, coords, tile, rotation):
        """
        Place une tuile à une position donnée avec une rotation spécifique sur le plateau.
        :param coords: Les coordonnées où placer la tuile (objet `Coords`).
        :param tile: La tuile à placer.
        :param rotation: La rotation à appliquer à la tuile (0, 90, 180, 270 degrés).
        """
        # Appliquer la rotation à la tuile
        for _ in range(rotation // 90):
            tile.rotate_clockwise()

        # Vérifier si la position est valide et disponible
        if self._tiles[coords.row][coords.column] is not None:
            raise ValueError(f"La position {coords} est déjà occupée.")

        # Placer la tuile sur le plateau
        self._tiles[coords.row][coords.column] = tile