from typing import Callable
from hypothesis import given, strategies as st, assume
from gp_db.database import SemanticTrackerDB

@st.composite
def semantics_and_type_pairs(draw: Callable) -> tuple[list, type]:
    semantics_type = draw(st.sampled_from([bool, int, str]))
    semantics_list = draw(st.lists(st.from_type(semantics_type), min_size=1))
    return semantics_list, semantics_type

@given(st.integers())
def test_constructor_takes_one_argument(semantics_length):
    SemanticTrackerDB(semantics_length)


class TestAddVariableMethod:
    def test_add_variable_is_attribute(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert hasattr(db, "add_variable")

    def test_add_variable_is_callable(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert callable(db.add_variable)

    @given(st.text(), semantics_and_type_pairs())
    def test_add_variable_takes_a_string_and_a_list(self, variable_name, semantic_list_and_type):
        semantic_list, semantic_type = semantic_list_and_type
        assume(len(variable_name) > 0)
        assume(len(semantic_list) > 0)
        db = SemanticTrackerDB(semantics_length=1)
        db.add_variable(variable_name, semantic_list, semantic_type)

    @given(st.text(), semantics_and_type_pairs())
    def test_add_variable_returns_an_integer(self, variable_name, semantic_list_and_type):
        semantic_list, semantic_type = semantic_list_and_type
        assume(len(variable_name) > 0)
        assume(len(semantic_list) > 0)
        db = SemanticTrackerDB(semantics_length=1)
        semantics_id = db.add_variable(variable_name, semantic_list, semantic_type)
        assert isinstance(semantics_id, int)