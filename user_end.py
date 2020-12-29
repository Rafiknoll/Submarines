from online_client import OnlineClient


def main():
    online_client = OnlineClient()
    online_client.find_match_by_listening()
    print("matched!")


if __name__ == "__main__":
    main()
