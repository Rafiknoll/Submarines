from online_client import OnlineClient
from board import BoardManager
from predifined_submarines import insert_predefined_submarines
from exceptions import EnemySurrenderedException, SelfSurrenderException
from consts import AttackResult, SURRENDER_FLAG
import sys

SURRENDER_LOCATION = (15, 15)  # [This is direct by-product of the surrender flag in the protocol


class GameManager:

    def __init__(self, online_client: OnlineClient, board: BoardManager):
        self.online_client = online_client
        self.board = board

    def init_game(self):
        submarine_lengths = self.online_client.decide_submarines_lengths()
        print(f"Please insert locations for submarines with the following lengths {submarine_lengths}:")
        # We will actually skip this because this is very tiresome for testing
        print("Inserting predefined submarines instead")
        insert_predefined_submarines(self.board)
        print("Ready to start")
        # The skip ends here
        self.online_client.send_flag()
        self.online_client.wait_for_flag()
        print("Game starting")

    def loop_turns(self):
        try:
            while not self.is_lost():
                if self.online_client.is_passive_side:
                    self.execute_attack()
                    self.receive_attack()
                else:
                    self.receive_attack()
                    if not self.is_lost():
                        self.execute_attack()
        except EnemySurrenderedException:
            print("Your enemy surrendered")
        except SelfSurrenderException:
            print("You surrendered")

    def execute_attack(self):
        row = int(input("Input row to attack: "))
        column = int(input("Input column to attack: "))
        location = (row, column)
        self.online_client.send_attack(location)
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
        print("Enemy turn")
        location = self.online_client.receive_attack()
        if location == SURRENDER_FLAG:
            raise EnemySurrenderedException
        print(f"Enemy targets location : {location}")
        attack_results = self.board.get_result_of_being_attacked(location)
        print(self.parse_attack_results(attack_results))
        self.online_client.send_response_for_attack(attack_results)

    def is_lost(self):
        return all([submarine.is_dead() for submarine in self.board.submarines])

    @staticmethod
    def parse_attack_results(attack_results):
        if AttackResult(attack_results) == AttackResult.MISS:
            ret_str = "Missed"
        else:
            ret_str = "Hit"
            if AttackResult(attack_results) == AttackResult.KILL:
                ret_str += ", Submarine sunk!"
        return ret_str


def main():
    board = BoardManager()
    if len(sys.argv) > 1:
        print(f"Connecting to {sys.argv[1]}")
        online_client = OnlineClient(sys.argv[1])
    else:
        print("Looking for game")
        online_client = OnlineClient()
    online_client.match_with_another_player()
    print("Connection established")
    game_manager = GameManager(online_client, board)
    game_manager.init_game()
    game_manager.loop_turns()


if __name__ == "__main__":
    main()
