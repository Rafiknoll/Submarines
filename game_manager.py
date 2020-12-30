"""
Name:       game_manager.py

Purpose:    Provides the main manager of the submarine game

Usage:      from game_manager import GameManager

Author:     Rafael Knoll
"""
from online_client import OnlineClient
from board import BoardManager
from exceptions import EnemySurrenderedException, SelfSurrenderException, LocationOccupiedException
from consts import AttackResult, SURRENDER_FLAG
from utils import int_input

SURRENDER_LOCATION = (15, 15)  # [This is direct by-product of the surrender flag in the protocol]


class GameManager:
    """
    Controls the flow of the game, utilizing the board and online client to handle offline and online logic
    """

    def __init__(self, online_client: OnlineClient, board: BoardManager):
        self.online_client = online_client
        self.board = board

    def init_game(self):
        """
        Handles placing the submarines and preparing for the first attack interaction
        :return: None
        """
        submarine_lengths = self.online_client.decide_submarines_lengths()
        print(f"Please insert locations for submarines with the following lengths {submarine_lengths}:")
        self.read_submarines(submarine_lengths)
        print("Waiting for the other player to get ready")
        self.online_client.send_flag()
        self.online_client.wait_for_flag()
        print("Game starting")

    def read_submarines(self, submarines_lengths):
        """
        Reads the required submarines from the user
        :return: None
        """
        for submarine_length in submarines_lengths:
            self.read_submarine(submarine_length)

    def read_submarine(self, submarine_length):
        """
        Reads a single submarine from the user
        :return: None
        """
        while True:
            print(f"Enter coordinates for a submarine of length {submarine_length}")
            locations = []
            for _ in range(submarine_length):
                row = int_input("Enter row number: ")
                column = int_input("Enter column number: ")
                locations.append((row, column))
            try:
                self.board.place_submarine(locations)
                return
            except ValueError as error:
                print(error.args[0])
            except KeyError as error:
                print(error.args[0])
            except LocationOccupiedException as error:
                print(error.args[0])

    def loop_turns(self):
        """
        Loops turns until there is a winner
        :return: None
        """
        try:
            while not self.is_lost():
                if self.online_client.is_passive_side:
                    self.execute_attack()
                    self.receive_attack()
                else:
                    self.receive_attack()
                    if not self.is_lost():
                        self.execute_attack()

            # If we got here, that's a loss
            print("You lost!")
            self.online_client.send_attack(SURRENDER_LOCATION)
        except EnemySurrenderedException:
            print("Your enemy surrendered or lost")
        except SelfSurrenderException:
            print("You surrendered")
        except ConnectionAbortedError:
            print("Your enemy disconnected. You won.")

    def execute_attack(self):
        """
        Requests attack location from the user and displays the results of the attack
        :return: None
        """
        while True:
            row = int_input("Input row to attack: ")
            column = int_input("Input column to attack: ")
            location = (row, column)
            try:
                self.online_client.send_attack(location)
                break
            except TypeError as error:
                print(error.args[0])
        if location == SURRENDER_LOCATION:
            raise SelfSurrenderException
        attack_results = self.online_client.receive_response_for_attack()

        # The below if statement is for protocol compatibility. There is no way it will happen in this implementation
        if attack_results == SURRENDER_FLAG:
            raise EnemySurrenderedException

        print(self.parse_attack_results(attack_results))
        self.board.save_result_of_attacking(location, attack_results)
        if self.board.submarines_to_sink == 0:
            print("You won!")

    def receive_attack(self):
        """
        Receives an attack from the enemy, acts accordingly and displays the results
        :return: None
        """
        print("Enemy turn")
        location = self.online_client.receive_attack()
        if location == SURRENDER_FLAG:
            raise EnemySurrenderedException
        print(f"Enemy targets location : {location}")
        attack_results = self.board.get_result_of_being_attacked(location)
        print(self.parse_attack_results(attack_results))
        self.online_client.send_response_for_attack(attack_results)

    def is_lost(self):
        """
        Checks if the player lost the game
        :return: True if the player lost
        """
        return all([submarine.is_dead() for submarine in self.board.submarines])

    @staticmethod
    def parse_attack_results(attack_results):
        """
        Parses the results of an attack into string
        :param attack_results: The results
        :return: The string
        """
        if AttackResult(attack_results) == AttackResult.MISS:
            ret_str = "Missed"
        else:
            ret_str = "Hit"
            if AttackResult(attack_results) == AttackResult.KILL:
                ret_str += ", Submarine sunk!"
        return ret_str
