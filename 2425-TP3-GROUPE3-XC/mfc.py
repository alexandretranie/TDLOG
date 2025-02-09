from game import Game  # Importer la classe Game depuis game.py
import player
import deck
import utils
import tile

# config.py
path_to_deck = "default.deck"


# Entry point of the program
if __name__ == "__main__":
    # Créer des instances de joueurs
    xclerc = player.HumanPlayer(name="xclerc", color=player.Color.BLUE, num_pawns=8)
    ai_player = player.AIPlayer(color=player.Color.RED, num_pawns=8, level=player.AILevel.EASY)
    random_player = player.RandomPlayer(color=player.Color.YELLOW, num_pawns=8)

    # Créer une instance de Game avec la liste des joueurs et le chemin vers le fichier de tuiles
    game_state = Game(players=[xclerc, ai_player, random_player], deck_path=path_to_deck)

    # Afficher l'état du jeu
    game_state.display()

    # Charger et afficher les tuiles depuis le fichier deck
    try:
        tiles = deck.load_tiles(path_to_deck)
        print(f"{len(tiles)} tuiles chargées.")
        for i, til in enumerate(tiles):
            print(f"Tuile {i+1}: {til}")
    except Exception as e:
        print(f"Erreur lors du chargement des tuiles : {e}")

    # Parcourir toutes les tuiles et les afficher sous forme de grille de caractères
    for i, tile_to_display in enumerate(tiles):
        print(f"Tuile {i + 1} :")

        # Créer une grille de caractères pour afficher la tuile
        chars = utils.make_2d_chars(height=tile.TILE_HEIGHT, width=tile.TILE_WIDTH, value='.')
        chars = utils.make_2d_chars(height=tile.TILE_HEIGHT, width=tile.TILE_WIDTH, value='.')


        # Afficher la tuile sur la grille de caractères
        tile_to_display.display_in_chars(chars, start_row=0, start_column=0)

        # Imprimer la grille de caractères pour la tuile
        print("\n".join("".join(row) for row in chars))
        print("\n" + "-"*20 + "\n")  # Séparation entre les tuiles
