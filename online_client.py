"""
Name:       online_client.py

Purpose:    Provides the online client for the submarine game

Usage:      from online_client import OnlineClient

Author:     Rafael Knoll
"""
import socket
from exceptions import ConnectionNotMadeYetException
from utils import num_to_byte, byte_to_num

from consts import GAME_PORT, DEFAULT_SUBMARINES_SIZES, GAME_FLAG, SURRENDER_FLAG

ANY_IP = "0.0.0.0"
HEX_BASE = 16
HEX_RANGE = range(HEX_BASE)


class OnlineClient:
    """
    Handles all online interactions between the players
    """

    def __init__(self, other_player_ip=None):
        self.other_player_socket = None
        self.other_player_ip = other_player_ip
        self.is_passive_side = other_player_ip is None

    def __verify_has_connection(self):
        """
        Checks whenever we already made a connection with another player or not. Should be called at the start of
        each function that uses the connection
        :return: None
        :raises: ConnectionNotMadeYetException if connection was not made yet
        """
        if self.other_player_socket is None:
            raise ConnectionNotMadeYetException

    def __find_match_by_listening(self):
        """
        Listens for another player to match with him and open a socket with him
        :return: None
        """
        listening_socket = socket.socket()
        listening_socket.bind((ANY_IP, GAME_PORT))
        listening_socket.listen()
        self.other_player_socket, self.other_player_ip = listening_socket.accept()

    def __connect_to_other_player(self, target_ip):
        """
        Actively connects to another player that is listening for connection, and opens a socket with him
        :param target_ip: The IP of the listener
        :return: None
        """
        self.other_player_socket = socket.socket()
        self.other_player_socket.connect((target_ip, GAME_PORT))

    def __receive_submarines_lengths(self):
        """
        Passively listens to receive an array of lengths of the submarines in the game
        :return: The array of lengths of the submarines
        """
        self.__verify_has_connection()
        number_of_submarines = byte_to_num(self.other_player_socket.recv(1))
        submarines_lengths = []
        for _ in range(number_of_submarines):
            submarines_lengths.append(byte_to_num(self.other_player_socket.recv(1)))

        return submarines_lengths

    def __send_submarines_lengths(self, submarines_lengths):
        """
        Sends an array of submarine lengths to the other player
        :param submarines_lengths: The array of lengths
        :return: None
        """
        self.__verify_has_connection()
        self.other_player_socket.send(num_to_byte(len(submarines_lengths)))
        for submarine_length in submarines_lengths:
            self.other_player_socket.send(num_to_byte(submarine_length))

    def match_with_another_player(self):
        """
        A front for the function to connect to another player for both the passive and active side
        :return: None
        """
        if self.is_passive_side:
            self.__find_match_by_listening()
        else:
            self.__connect_to_other_player(self.other_player_ip)

    def decide_submarines_lengths(self):
        """
        A front for the function to decide the lengths of all submarines, for both the passive and active side
        :return: The array of lengths
        """
        if self.is_passive_side:
            return self.__receive_submarines_lengths()
        else:
            submarines_lengths = DEFAULT_SUBMARINES_SIZES
            self.__send_submarines_lengths(submarines_lengths)
            return submarines_lengths

    def send_flag(self):
        """
        Sends the flag indicating it is ready to play
        :return: None
        """
        self.__verify_has_connection()
        self.other_player_socket.send(num_to_byte(GAME_FLAG))

    def wait_for_flag(self):
        """
        Waits for the flag indicating the other player is ready to play
        :return: None
        """
        self.__verify_has_connection()
        other_side_message = 0
        while other_side_message != GAME_FLAG:
            other_side_message = byte_to_num(self.other_player_socket.recv(1))

    def send_attack(self, location):
        """
        Sends an attack to the other player
        :param location: The location to attack
        :return: None
        """
        self.__verify_has_connection()
        row, column = location
        if row not in HEX_RANGE or column not in HEX_RANGE:
            raise TypeError("Location index out of possible hexadecimal range")

        attack_number = row * HEX_BASE + column
        self.other_player_socket.send(num_to_byte(attack_number))

    def receive_attack(self):
        """
        Receives an attack from the enemy player
        :return: The location of the attack
        """
        self.__verify_has_connection()
        message = byte_to_num(self.other_player_socket.recv(1))
        if message == SURRENDER_FLAG:
            return SURRENDER_FLAG

        row = message // HEX_BASE
        column = message % HEX_BASE
        return row, column

    def send_response_for_attack(self, response):
        """
        Sends a response code for an attack
        :param response: The response code
        :return: None
        """
        self.__verify_has_connection()
        self.other_player_socket.send(num_to_byte(response.value))

    def receive_response_for_attack(self):
        """
        Receives a response code for an attack
        :return: The response code
        """
        self.__verify_has_connection()
        return byte_to_num(self.other_player_socket.recv(1))
