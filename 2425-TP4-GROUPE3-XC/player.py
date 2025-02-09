import enum
import random

"""
This module defines the different kinds of players (both their state and
behavior).
"""


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
    """
    Parent class for all kinds of player; the state of a player consists of:
    - a color (immutable);
    - a number of pawns still to place (mutable).
    """

    def __init__(self, color, num_pawns):
        assert num_pawns > 0, "invalida num_pawns"
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
        assert value >= 0, "invalid num_pawns"
        self._num_pawns = value


class HumanPlayer(Player):
    """
    A human player is a player additionally defined by a name (which is not
    mutable). Its behavior is read from the standard input.
    """

    def __init__(self, color, num_pawns, name):
        super().__init__(color, num_pawns)
        assert name.strip(), "empty name"
        self._name = name

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name
    
    def play(self, possible_moves):
        """
        Affiche les coups possibles et demande à l'utilisateur de choisir.
        """
        print(f"{self._name}, voici les coups possibles :")
        for idx, move in enumerate(possible_moves):
            # Affiche les informations de chaque coup (position et rotation)
            print(f"{idx}: Position {move[0]}, Rotation {move[1]}")
        choice = int(input("Entrez le numéro du coup que vous voulez jouer : "))
        return possible_moves[choice]  # Retourne un tuple (position, rotation)


class RandomPlayer(Player):
    """
    A random player, provided mainly for testing, is a player whose behavior is
    random.
    """

    def __init__(self, color, num_pawns):
        super().__init__(color, num_pawns)

    def __str__(self):
        return "random"
    
    def play(self, possible_moves):
        """
        Choisit un coup au hasard dans la liste des coups possibles.
        """
        return random.choice(possible_moves)


class AILevel(enum.Enum):
    """
    The possible difficulty level of an AI player.
    """

    EASY = "easy"
    HARD = "hard"


class AIPlayer(Player):
    """
    An AI player is a player additionally defined by a difficulty level.
    """

    def __init__(self, color, num_pawns, level):
        super().__init__(color, num_pawns)
        self._level = level

    @property
    def level(self):
        return self._level

    def __str__(self):
        return f"AI ({self._level})"

    def evaluate_pawn_placement(position, player_color, board):
        """
        Évalue combien de pions du joueur seront placés à cette position.
    
        :param position: Coordonnées (row, column) de la position où la tuile sera placée.
        :param player_color: La couleur du joueur.
        :param board: L'état actuel du plateau (grille de tuiles).
    
        :return: Le nombre de pions que le joueur peut placer à cette position.
        """
        row, col = position
        score = 0

        # Vérifier les connexions possibles aux tuiles adjacentes
        adjacent_tiles = [
            (row - 1, col),  # Nord
            (row + 1, col),  # Sud
            (row, col - 1),  # Ouest
            (row, col + 1)   # Est
        ]

        for adj_row, adj_col in adjacent_tiles:
            # Vérifier que la position adjacente est valide et sur le plateau
            if 0 <= adj_row < board._height and 0 <= adj_col < board._width:
                adjacent_tile = board._tiles[adj_row][adj_col]
                if adjacent_tile is not None:
                    # Si la tuile adjacente est occupée par le même joueur
                    for link in adjacent_tile.links:
                        if link.color == player_color:
                            # Augmenter le score si la connexion est bénéfique
                            score += 1

        return score
    

    def evaluate_opponent_impact(position, player_color, board, players):
        """
        Évalue l'impact négatif d'un coup sur les adversaires.
    
        :param position: Coordonnées (row, column) de la position où la tuile sera placée.
        :param player_color: La couleur du joueur.
        :param board: L'état actuel du plateau (grille de tuiles).
        :param players: La liste des joueurs dans la partie.
    
        :return: Un score négatif si cela aide les adversaires.
        """
        row, col = position
        negative_impact = 0

        # Vérifier les connexions possibles aux tuiles adjacentes
        adjacent_tiles = [
            (row - 1, col),  # Nord
            (row + 1, col),  # Sud
            (row, col - 1),  # Ouest
            (row, col + 1)   # Est
        ]

        for adj_row, adj_col in adjacent_tiles:
            # Vérifier que la position adjacente est valide et sur le plateau
            if 0 <= adj_row < board._height and 0 <= adj_col < board._width:
                adjacent_tile = board._tiles[adj_row][adj_col]
                if adjacent_tile is not None:
                    # Vérifier si l'adversaire est présent dans les connexions de cette tuile
                    for link in adjacent_tile.links:
                        if link.color != player_color:  # L'adversaire est connecté ici
                            # Ajouter un score négatif si cela avantage un adversaire
                            negative_impact -= 1

        return negative_impact


    def evaluate_move_fn(move, player_color, difficulty, board,players):
        """
        Évalue un coup donné en fonction du niveau de difficulté.
        - move : un tuple (position, rotation)
        - player_color : la couleur du joueur effectuant le coup
        - difficulty : 'easy' ou 'hard'
        """

        position, rotation = move  # Décomposer le tuple (position, rotation)

        # Critère de base : dans tous les cas, on évalue la position en fonction des pions que cela place
        score = evaluate_pawn_placement(position, player_color, board)

        if difficulty == 'easy':
            # Niveau EASY : se concentrer uniquement sur le placement de pions du joueur
            return score  # Simplement maximiser le nombre de pions du joueur
        elif difficulty == 'hard':
            # Niveau HARD : minimiser les pions adverses et maximiser les pions du joueur
            score -= evaluate_opponent_impact(position, player_color, board, players)  # Pénaliser si cela aide les adversaires
            return score
    
    def play(self, possible_moves, evaluate_move_fn):
        """
        Pour un joueur IA, sélectionne un coup en fonction du niveau de difficulté.
        - Niveau EASY : Choisit le coup qui place le maximum de pions.
        - Niveau HARD : Maximise les pions du joueur et minimise ceux de l'adversaire.
        
        :param possible_moves: Liste des coups possibles.
        :param evaluate_move_fn: Fonction pour évaluer les coups.
        :return: Le coup choisi.
        """
        if self._level == AILevel.EASY:
            # Choisir le coup qui place le maximum de pions pour le joueur
            best_move = max(possible_moves, key=lambda move: evaluate_move_fn(move, self.color, 'easy'))
        elif self._level == AILevel.HARD:
            # Choisir le coup qui maximise les pions du joueur et minimise ceux des adversaires
            best_move = max(possible_moves, key=lambda move: evaluate_move_fn(move, self.color, 'hard'))
        return best_move
