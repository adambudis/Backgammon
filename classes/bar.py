from classes.spike import Spike


class Bar(Spike):
    def __init__(self, index: int, max_size: int) -> None:
        super().__init__(index, max_size)

    def __str__(self) -> str:
        return f"bar: {self.size()}"