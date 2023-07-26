from typing import Callable


class SemanticsTrackerDB:
    def __init__(self) -> None:
        ...

    def add_semantics(self, semantics: list[int]) -> int:
        ...

    def get_semantics(self, semantics_id: int) -> list:
        ...

    def combine_semantics(self, from_function: Callable, ancestors: list[int]) -> int:
        ...