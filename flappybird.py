import sys

from ai_game import AiGame
from single_player_game import SinglePlayerGame

GAME_MODE_MAP = {
    "a": AiGame,
    "s": SinglePlayerGame
}


def main() -> None:
    game_mode = sys.argv

    if len(game_mode) <= 1:
        game = GAME_MODE_MAP["s"]()
    else:
        game = GAME_MODE_MAP[game_mode[1].lower()]()

    print(game)
    game.run()


if __name__ == "__main__":
    main()
