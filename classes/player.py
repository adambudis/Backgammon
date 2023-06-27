from abc import ABC, abstractmethod
from classes.bar import Bar


class Player(ABC):
    def __init__(self, color: str, move_direction: int, bar_index: int, home_index: int, home_board: range, stones_kicked=0) -> None:
        self._color = color
        self._move_direction = move_direction
        self._bar = Bar(bar_index, 15)
        self._home_index = home_index
        self._home_board = home_board
        self._stones_kicked = stones_kicked

    @property
    def color(self) -> str:
        return self._color
    
    @property
    def move_direction(self) -> int:
        return self._move_direction
    
    @property
    def bar(self) -> Bar:
        return self._bar
    
    @property
    def home_index(self) -> int:
        return self._home_index
    
    @property
    def home_board(self) -> range:
        return self._home_board

    @property
    def stones_kicked(self) -> int:
        return self._stones_kicked

    @abstractmethod
    def play_move(self, legal_moves: dict) -> list:
        ...
    
    def increase_number_of_stones_kicked(self) -> None:
        self._stones_kicked += 1
    
    def __str__(self) -> str:
        return f"{self._color.upper()}"