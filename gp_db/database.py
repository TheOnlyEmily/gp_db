from typing import Callable


class SemanticTrackerDB:
    def __init__(self, semantics_length: int) -> None:
        assert type(semantics_length) is int, "semantics length must be of type integer"
        assert semantics_length > 0, "semantics length must be postive and non-zero"
        self._next_id: int = 0
        self._semantics_length = semantics_length

    def add_variable(self, semantics: list) -> int:
        assert type(semantics) is list, "semantics must be of type list"
        assert len(semantics) == self._semantics_length, f"expected semantics of length {self._semantics_length} not {len(semantics)}"
        semantics_id = self._next_id
        self._next_id += 1
        return semantics_id

    def add_function(self, name: str, function: Callable) -> int:
        assert type(name) is str, "name must be of type string"
        assert name is not '', "empty string is not a valid name"
        assert callable(function), "function must be callable"

    def combine_semantics(self, func_name: str, semantics_ids: list[int]) -> int:
        assert type(func_name) is str, "function name should be of type string"
        assert func_name is not '', "function name should not be empty string"
        assert type(semantics_ids) is list, "semantics ids should be of type list"
        return 0