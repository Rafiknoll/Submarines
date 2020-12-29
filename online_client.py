import socket

GAME_PORT = 25565
ANY_IP = "0.0.0.0"


class OnlineClient:

    def __init__(self):
        self.other_player_socket = None

    def find_match_by_listening(self):
        listening_socket = socket.socket()
        listening_socket.bind((ANY_IP, GAME_PORT))
        listening_socket.listen()
        self.other_player_socket, _ = listening_socket.accept()
