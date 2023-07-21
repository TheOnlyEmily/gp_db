class SemanticTrackerDB:
    def __init__(self, semantics_length: int) -> None:
        if type(semantics_length) is not int:
            raise SemanticDbInitError("semantics length must be of type int")
        if semantics_length < 1:
            raise SemanticDbInitError("semantics length must be postive and non-zero")
        self._next_id: int = 0
        self._semantics_length = semantics_length

    def add_variable(self, name: str, semantics: list, semantics_type: type) -> int:
        if name == '':
            raise SemanticEntryError("empty string is not a valid name")
        if len(semantics) != self._semantics_length:
            raise SemanticEntryError(f"expected semantics of length {self._semantics_length} not {len(semantics)}")
        semantics_id = self._next_id
        self._next_id += 1
        return semantics_id


class SemanticEntryError(Exception): ...


class SemanticDbInitError(Exception): ...