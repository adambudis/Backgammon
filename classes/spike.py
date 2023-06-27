from classes.stone import Stone


class Spike:
    def __init__(self, index: int, max_size=5) -> None:
        self._index = index
        self._stones = []
        self._max_size = max_size

    def push_stone(self, stone: Stone) -> None:
        if len(self._stones) <= self._max_size:
            self._stones.append(stone)

    def pop_stone(self) -> Stone:
        if len(self._stones):
            return self._stones.pop()

    def get_stone(self) -> Stone:
        if len(self._stones):
            return self._stones[-1]

    def is_empty(self) -> bool:
        return len(self._stones) == 0

    def size(self) -> int:
        return len(self._stones)

    @property
    def index(self) -> int:
        return self._index
    
    @property
    def stones(self) -> list:
        return self._stones

    def __str__(self) -> str:
        return f"{self._index}: {[str(stone) for stone in self._stones]}"