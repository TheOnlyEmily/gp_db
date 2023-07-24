from typing import Callable


class SemanticTrackerDB:
    def __init__(self, semantics_length: int) -> None:
        if type(semantics_length) is not int:
            raise SemanticDbInitError("semantics length must be of type int")
        if semantics_length < 1:
            raise SemanticDbInitError("semantics length must be postive and non-zero")
        self._next_id: int = 0
        self._semantics_length = semantics_length

    def add_variable(self, semantics: list) -> int:
        if not isinstance(semantics, list):
            raise SemanticEntryError("semantics must be of type list")
        if len(semantics) != self._semantics_length:
            raise SemanticEntryError(f"expected semantics of length {self._semantics_length} not {len(semantics)}")
        semantics_id = self._next_id
        self._next_id += 1
        return semantics_id

    def add_function(self, name: str, function: Callable) -> int:
        if not isinstance(name, str):
            raise SemanticEntryError("function name must be of type string")
        if name == '':
            raise SemanticEntryError("empty string is not a valid name")
        if not callable(function):
            raise SemanticEntryError("function must be callable")


class SemanticEntryError(Exception): ...


class SemanticDbInitError(Exception): ...