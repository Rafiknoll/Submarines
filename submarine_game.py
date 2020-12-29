from online_client import OnlineClient
from board import BoardManager


def main():
    board = BoardManager()
    online_client = OnlineClient()
    online_client.match_with_another_player()
    print(online_client.decide_submarines_lengths())


if __name__ == "__main__":
    main()
