import board
import deck
import random

"""
This module defines the state of an in-progress game, as well as the game main
loop.
"""

NUM_PAWNS = 8  # Initial number of pawns per player


class Game:
    """
    The state of the game is defined by:
    - a list of players;
    - a board;
    - a deck of tiles.
    """

    def __init__(self, players, deck_path):
        """
        Create a game from a list of players, and an optional path to a file
        with the definition of the deck. If no path is provided, the default
        deck is implicitly used. Raises `deck.InvalidFormat` if the deck file
        does not follow the expected specification.
        """
        assert len(players) > 0, "empty players"
        assert len(set(map(lambda p: p.color, players))) == len(
            players
        ), "duplicate player color"
        self._players = players
        self._board = board.Board()
        self._deck = (
            deck.load_tiles(deck_path) if deck_path is not None else deck.make_tiles()
        )
        random.shuffle(self._deck)
        self._board[board.Coords(row=0, column=0)] = self._deck.pop()
        self._current_player_index = 0
        height = 5
        width = 5
        self._tiles = [[None for _ in range(width)] for _ in range(height)]
    
    def current_player(self):
        """
        Retourne le joueur qui doit jouer actuellement.
        """
        return self._players[self._current_player_index]

    def next_turn(self):
        """
        Passe au tour suivant en changeant le joueur actif.
        """
        self._current_player_index = (self._current_player_index + 1) % len(self._players)

    def get_possible_moves(self):
        """
        Génère tous les coups possibles pour le joueur en cours. 
        Retourne une liste de tuples (position, rotation).
        """
        # Obtenez toutes les positions adjacentes où une tuile peut être placée
        possible_positions = self._board.get_adjacent_positions()

        possible_moves = []
        for position in possible_positions:
            # Pour chaque position, tester toutes les rotations possibles
            for rotation in [0, 90, 180, 270]:
                possible_moves.append((position, rotation))  # Chaque coup est un tuple (position, rotation)
        
        return possible_moves

    def display(self):
        """
        Print the board and key info about the players onto the standard output.
        """
        self._board.display()
        print()
        for player_ in self._players:
            print(f"{player_} ({player_.color.value}): {player_.num_pawns}")
        print()

    def apply_move(self, move):
        """
        Applique un coup donné sur le plateau.
    
        :param move: Un tuple (position, rotation) représentant le coup à jouer.
        """

        position, rotation = move
        # Récupérer les attributs x et y de l'objet Coords
        row = position.row
        col = position.column
        print(f"Move position: {position}, rotation: {rotation}")

        # Récupérer le joueur actuel et la tuile correspondante
        current_player = self.current_player()
        if current_player.num_pawns == 0:
            raise ValueError(f"{current_player} n'a plus de pions à placer.")
        
        # Vérifier que la position est valide sur le plateau
        if not (0 <= row < self._board._height and 0 <= col < self._board._width):
            raise ValueError(f"La position {position} est en dehors des limites du plateau.")
        
        # Vérifier que le deck n'est pas vide avant de piocher
        if not self._deck:
            raise ValueError("Le deck est vide. Impossible de tirer une nouvelle tuile.")
        
        # Créer une nouvelle tuile et l'appliquer avec la rotation donnée
        new_tile = self._deck.pop()

        if rotation % 90 != 0:
            raise ValueError("La rotation doit être un multiple de 90 degrés.")
        
        for _ in range(rotation // 90):
            new_tile.rotate_clockwise()

        # Placer la tuile sur le plateau
        self._board.place_tile_with_rotation(position, new_tile, rotation)

        # Mettre à jour les pions du joueur
        current_player.num_pawns -= 1

        # Confirmation du placement
        print(f"{current_player} a placé une tuile en {position} avec une rotation de {rotation} degrés. "
          f"Il reste {current_player.num_pawns} pions.")
