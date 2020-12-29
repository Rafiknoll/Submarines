import socket
from exceptions import ConnectionNotMadeYetException
from utils import num_to_byte, byte_to_num

from consts import GAME_PORT, DEFAULT_SUBMARINES_SIZES, GAME_FLAG

ANY_IP = "0.0.0.0"


class OnlineClient:

    def __init__(self, other_player_ip=None):
        self.other_player_socket = None
        self.other_player_ip = other_player_ip
        self.is_passive_side = other_player_ip is None

    def __verify_has_connection(self):
        if self.other_player_socket is None:
            raise ConnectionNotMadeYetException

    def __find_match_by_listening(self):
        listening_socket = socket.socket()
        listening_socket.bind((ANY_IP, GAME_PORT))
        listening_socket.listen()
        self.other_player_socket, self.other_player_ip = listening_socket.accept()

    def __connect_to_other_player(self, target_ip):
        self.other_player_socket = socket.socket()
        self.other_player_socket.connect((target_ip, GAME_PORT))

    def __receive_submarines_lengths(self):
        self.__verify_has_connection()
        number_of_submarines = byte_to_num(self.other_player_socket.recv(1))
        submarines_lengths = []
        for _ in range(number_of_submarines):
            submarines_lengths.append(byte_to_num(self.other_player_socket.recv(1)))

        return submarines_lengths

    def __send_submarines_lengths(self, submarines_lengths):
        self.__verify_has_connection()
        self.other_player_socket.send(num_to_byte(len(submarines_lengths)))
        for submarine_length in submarines_lengths:
            self.other_player_socket.send(num_to_byte(submarine_length))

    def match_with_another_player(self):
        if self.is_passive_side:
            self.__find_match_by_listening()
        else:
            self.__connect_to_other_player(self.other_player_ip)

    def decide_submarines_lengths(self):
        if self.is_passive_side:
            return self.__receive_submarines_lengths()
        else:
            submarines_lengths = DEFAULT_SUBMARINES_SIZES
            self.__send_submarines_lengths(submarines_lengths)
            return submarines_lengths

    def send_flag(self):
        self.__verify_has_connection()
        self.other_player_socket.send(num_to_byte(GAME_FLAG))

    def wait_for_flag(self):
        self.__verify_has_connection()
        other_side_message = 0
        while other_side_message != GAME_FLAG:
            other_side_message = self.other_player_socket.recv(1)
