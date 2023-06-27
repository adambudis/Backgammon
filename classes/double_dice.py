import random


class DoubleDice:
    def throw_double_dice(self) -> list:
        first_roll = random.randint(1, 6)
        second_roll = random.randint(1, 6)
        if first_roll == second_roll:
            return [first_roll for _ in range(4)]
        else:
            return [first_roll, second_roll]