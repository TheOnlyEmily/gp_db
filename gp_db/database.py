import networkx as nx
from typing import Callable


class SemanticsTracker:
    def __init__(self) -> None:
        self._semantics_tree = nx.DiGraph()
        self._semantics_list: list[int] = []

    def add_semantics(self, semantics: list[int]) -> int:
        sem_id: int = len(self._semantics_list)
        self._semantics_list.append(semantics)
        self._semantics_tree.add_node(sem_id)
        return sem_id

    def get_semantics(self, semantics_id: int) -> list:
        return self._semantics_list[semantics_id]

    def combine_semantics(self, from_function: Callable, ancestors: list[int]) -> int:
        from_function_args = (self.get_semantics(a) for a in ancestors)
        sem_id: int = self.add_semantics(from_function(*from_function_args))

        ancestor_connections = ((a, sem_id) for a in ancestors)
        self._semantics_tree.add_edges_from(ancestor_connections)

        return sem_id