from typing import Callable
from hypothesis import given, strategies as st, assume
from gp_db.database import SemanticTrackerDB

@st.composite
def semantics_info(draw: Callable) -> tuple[list, type]:
    semantics_type = draw(st.sampled_from([bool, int, str]))
    semantics_list = draw(st.lists(st.from_type(semantics_type), min_size=1))
    variable_name = draw(st.text())
    return semantics_list, semantics_type, variable_name

@given(st.integers())
def test_constructor_takes_one_argument(semantics_length):
    assume(semantics_length > 0)
    
    SemanticTrackerDB(semantics_length)


class TestAddVariableMethod:
    def test_add_variable_is_attribute(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert hasattr(db, "add_variable")

    def test_add_variable_is_callable(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert callable(db.add_variable)

    @given(semantics_info())
    def test_add_variable_takes_a_string_and_a_list(self, semantics_info):
        semantic_list, semantic_type, variable_name = semantics_info
        assume(len(variable_name) > 0)
        assume(len(semantic_list) > 0)
        db = SemanticTrackerDB(semantics_length=1)
        db.add_variable(variable_name, semantic_list, semantic_type)

    @given(semantics_info())
    def test_add_variable_returns_an_integer(self, semantics_info):
        semantic_list, semantic_type, variable_name = semantics_info
        assume(len(variable_name) > 0)
        assume(len(semantic_list) > 0)
        db = SemanticTrackerDB(semantics_length=1)
        semantics_id = db.add_variable(variable_name, semantic_list, semantic_type)
        assert isinstance(semantics_id, int)

    @given(semantics_info(), semantics_info())
    def test_add_variable_returns_a_different_integer_for_each_call(self, semantics_info1, semantics_info2):
        semantic_list1, semantic_type1, variable_name1 = semantics_info1
        semantic_list2, semantic_type2, variable_name2 = semantics_info2
        assume(len(variable_name1) > 0)
        assume(len(semantic_list1) > 0)
        assume(len(variable_name2) > 0)
        assume(len(semantic_list2) > 0)
        assume(semantic_list1 != semantic_list2)
        assume(variable_name1 != variable_name2)
        db = SemanticTrackerDB(semantics_length=1)
        semantics_id1 = db.add_variable(variable_name1, semantic_list1, semantic_type1)
        semantics_id2 = db.add_variable(variable_name2, semantic_list2, semantic_type2)
        assert semantics_id1 != semantics_id2