class SemanticTrackerDB:
    def __init__(self, semantics_length: int) -> None:
        self._next_id: int = 0

    def add_variable(self, name: str, semantics: list, semantics_type: type) -> int:
        semantics_id = self._next_id
        self._next_id += 1
        return semantics_id