"""
Name:       submarine_game.py

Purpose:    The runnable of the submarine game

Usage:      python submarine_game.py [target_ip]

Author:     Rafael Knoll
"""
from game_manager import GameManager
from board import BoardManager
from online_client import OnlineClient
import sys

TARGET_IP_ARGV_INDEX = 1


def choose_online_mode():
    """
    Decides whenever to use the passive listening mode or actively connect to someone depending if there was an ip
    given as parameter or not
    :return: The online client for the game
    """
    if len(sys.argv) > 1:
        print(f"Connecting to {sys.argv[TARGET_IP_ARGV_INDEX]}")
        return OnlineClient(sys.argv[TARGET_IP_ARGV_INDEX])
    else:
        print("Looking for game")
        return OnlineClient()


def main():
    """
    Creates the board and online client for the game manager, connects to a player then runs the game
    :return: None
    """
    board = BoardManager()
    online_client = choose_online_mode()
    online_client.match_with_another_player()
    print("Connection established")
    game_manager = GameManager(online_client, board)
    game_manager.init_game()
    game_manager.loop_turns()


if __name__ == "__main__":
    main()
