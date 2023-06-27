from classes.player import Player


class HumanPlayer(Player):
    def __init__(self, color: str, move_direction: int, bar_index: int, home_index: int, home_board: range, stones_kicked=0) -> None:
        super().__init__(color, move_direction, bar_index, home_index, home_board, stones_kicked)

    def play_move(self, legal_moves: dict) -> list:
        move = check_input(input("Enter move: ").split(','))
        while True:
            if move[0] in ["exit", "save"]:
                return move[0]
            for key, values in legal_moves.items():
                if move[0] == key and move[1] in values:
                    print(move[0])
                    if move[0] == "bar":
                        return [self.bar.index, move[1]]
                    return move 
            else:
                move = check_input(input("Ilegal move, please enter valid move: ").split(','))

def check_input(items: list) -> list:
    result = []
    for item in items:
        try:
            result.append(int(item))
        except ValueError:
            result.append(item)
    return result