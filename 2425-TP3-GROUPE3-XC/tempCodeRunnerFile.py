class Game:
    def __init__(self, players,deck_path):
        self._players = players
        self._board = board.Board()
        # Charger les tuiles depuis le fichier deck_path
        try:
            self._deck = deck.load_tiles(deck_path)  # Utiliser load_tiles pour charger les tuiles
            print(f"{len(self._deck)} tuiles chargées avec succès.")
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement des tuiles : {e}")
        random.shuffle(self._deck)
        self._board[board.Coords(row=0, column=0)] = self._deck.pop()

    def display(self):
        self._board.display()
        print()
        for player_ in self._players:
            print(f"{player_} ({player_.color.value}): {player_.num_pawns}")
        print()