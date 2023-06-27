from typing import Any


class Stone:
    def __init__(self, color: str, position: int, history: list) -> None:
        self._color = color
        self._history = history
        self.add_positon_to_history(position)

    @property
    def color(self) -> str:
        return self._color

    @property
    def history(self) -> list:
        return self._history

    def delete_history(self) -> None:
        self._history = self._history[-1:]

    def add_positon_to_history(self, new_postion: Any) -> None:
        if len(self._history) != 0:
            if self._history[-1] != new_postion:
                self._history.append(new_postion)
                return
        else:
            self._history.append(new_postion)

    def __str__(self) -> str:
        return f"{self._color}"