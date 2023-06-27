import random
from classes.player import Player


class AIPlayer(Player):
    def __init__(self, color: str, move_direction: int, bar_index: int, home_index: int, home_board: range, stones_kicked=0) -> None:
        super().__init__(color, move_direction, bar_index, home_index, home_board, stones_kicked)

    def play_move(self, legal_moves: dict) -> list:
        random_key = random.choice(list(legal_moves.keys()))
        random_value = random.choice(legal_moves.get(random_key))
        if random_key == "bar":
            random_key = self.bar.index
        return [random_key, random_value]