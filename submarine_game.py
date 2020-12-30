from game_manager import GameManager
from board import BoardManager
from online_client import OnlineClient
import sys

TARGET_IP_ARGV_INDEX = 1


def choose_online_mode():
    if len(sys.argv) > 1:
        print(f"Connecting to {sys.argv[TARGET_IP_ARGV_INDEX]}")
        return OnlineClient(sys.argv[TARGET_IP_ARGV_INDEX])
    else:
        print("Looking for game")
        return OnlineClient()


def main():
    board = BoardManager()
    online_client = choose_online_mode()
    online_client.match_with_another_player()
    print("Connection established")
    game_manager = GameManager(online_client, board)
    game_manager.init_game()
    game_manager.loop_turns()


if __name__ == "__main__":
    main()
