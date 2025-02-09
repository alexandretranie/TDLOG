import deck
import game
import player
import sys

"""
This module is the main module of the program, and can be executed to play a
game of "My First Carcassonne".
"""

# Entry point of the program
if __name__ == "__main__":
    # create several players
    xclerc = player.HumanPlayer(
        color=player.Color.BLUE, num_pawns=game.NUM_PAWNS, name="xclerc"
    )
    ai_player = player.AIPlayer(
        color=player.Color.RED, num_pawns=game.NUM_PAWNS, level=player.AILevel.EASY
    )
    random_player = player.RandomPlayer(
        color=player.Color.YELLOW, num_pawns=game.NUM_PAWNS
    )
    # create a Game instance
    deck_path = sys.argv[1] if len(sys.argv) >= 2 else None
    try:
        game_state = game.Game(
            players=[xclerc, ai_player, random_player],
            deck_path=deck_path,
        )
    except deck.InvalidFormat as dif:
        print("*** deck error", dif)


"""# Function to test the game
def test_game():
    print("Initializing players...")
    
    # Create several players
    xclerc = player.HumanPlayer(
        color=player.Color.BLUE, num_pawns=game.NUM_PAWNS, name="xclerc"
    )
    ai_player = player.AIPlayer(
        color=player.Color.RED, num_pawns=game.NUM_PAWNS, level=player.AILevel.EASY
    )
    random_player = player.RandomPlayer(
        color=player.Color.YELLOW, num_pawns=game.NUM_PAWNS
    )

    # Display player information
    print(f"Human Player: {xclerc.name}, Color: {xclerc.color}, Pawns: {xclerc.num_pawns}")
    print(f"AI Player: {ai_player}, Level: {ai_player.level}, Pawns: {ai_player.num_pawns}")
    print(f"Random Player: {random_player}, Pawns: {random_player.num_pawns}")

    # Create a Game instance
    print("Initializing game...")
    deck_path = None  # Optionally, provide a deck path if needed
    try:
        game_state = game.Game(
            players=[xclerc, ai_player, random_player],
            deck_path=deck_path,
        )
        print("Game initialized successfully.")
    except deck.InvalidFormat as dif:
        print("*** deck error", dif)
        return

    # Simulate a few turns
    print("Starting simulation of the game...")
    try:
        for turn in range(5):  # Simulate 5 turns
            print(f"Turn {turn + 1}:")
            current_player = game_state.current_player()
            print(f"Current player: {current_player}")
            possible_moves = game_state.get_possible_moves()
            print(f"Possible moves for player {current_player}: {possible_moves}")

            if not possible_moves:
                print(f"No possible moves for player {current_player}")
                break

            chosen_move = current_player.play(possible_moves)
            game_state.apply_move(chosen_move)

            print(f"{current_player} played move at {chosen_move.position} with rotation {chosen_move.rotation}")

        print("Game simulation completed.")
    
    except Exception as e:
        print(f"An error occurred during the game simulation: {e}")

# Entry point of the program
if __name__ == "__main__":
    # Run the test function
    test_game()"""