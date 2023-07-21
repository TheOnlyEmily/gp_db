import pytest
from typing import Callable
from hypothesis import given, strategies as st, assume
from gp_db.database import SemanticTrackerDB, SemanticEntryError, SemanticDbInitError

@st.composite
def semantics_info(draw: Callable, semantics_length=None) -> tuple[list, type]:
    semantics_type = draw(st.sampled_from([bool, int, str]))
    if semantics_length is not None:
        semantics_list = draw(st.lists(st.from_type(semantics_type), min_size=semantics_length, max_size=semantics_length))
    else:
        semantics_list = draw(st.lists(st.from_type(semantics_type), min_size=1))
    variable_name = draw(st.text())
    return semantics_list, semantics_type, variable_name

class TestInitMethod:
    @given(st.integers())
    def test_constructor_takes_one_integer(self, semantics_length):
        assume(semantics_length > 0)
        
        SemanticTrackerDB(semantics_length)

    @given(st.integers())
    def test_constructor_raises_semantic_db_init_error_given_semantics_length_less_than_one(self, semantics_length):
        assume(semantics_length <= 0)

        with pytest.raises(SemanticDbInitError, match="semantics length must be postive and non-zero"): 
            SemanticTrackerDB(semantics_length)

    @given(st.one_of(st.booleans(), st.text(), st.floats()))
    def test_constructor_raises_semantic_db_init_error_given_semantics_length_not_of_type_int(self, semantics_length):
        with pytest.raises(SemanticDbInitError, match="semantics length must be of type int"): 
            SemanticTrackerDB(semantics_length)


class TestAddVariableMethod:
    def test_add_variable_is_attribute(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert hasattr(db, "add_variable")

    def test_add_variable_is_callable(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert callable(db.add_variable)

    @given(semantics_info(semantics_length=1))
    def test_add_variable_takes_a_string_and_a_list(self, semantics_info):
        semantic_list, semantic_type, variable_name = semantics_info
        assume(len(variable_name) > 0)
        db = SemanticTrackerDB(semantics_length=1)
        db.add_variable(variable_name, semantic_list, semantic_type)

    @given(semantics_info(semantics_length=1))
    def test_add_variable_raises_semantic_entry_error_given_empty_string(self, semantics_info):
        semantic_list, semantic_type, _ = semantics_info
        variable_name = ''
        db = SemanticTrackerDB(semantics_length=1)
        with pytest.raises(SemanticEntryError, match="empty string is not a valid name"):
            db.add_variable(variable_name, semantic_list, semantic_type)

    @given(semantics_info(), st.integers(min_value=1))
    def test_add_variable_raises_semantic_entry_error_given_list_of_wrong_size(self, semantics_info, expected_length):
        semantic_list, semantic_type, variable_name = semantics_info
        assume(len(variable_name) > 0)
        assume(len(semantic_list) != expected_length)
        db = SemanticTrackerDB(semantics_length=expected_length)
        with pytest.raises(SemanticEntryError, match=f"expected semantics of length {expected_length} not {len(semantic_list)}"):
            db.add_variable(variable_name, semantic_list, semantic_type)

    @given(semantics_info(semantics_length=1))
    def test_add_variable_returns_an_integer(self, semantics_info):
        semantic_list, semantic_type, variable_name = semantics_info
        assume(len(variable_name) > 0)
        db = SemanticTrackerDB(semantics_length=1)
        semantics_id = db.add_variable(variable_name, semantic_list, semantic_type)
        assert isinstance(semantics_id, int)

    @given(semantics_info(semantics_length=1), semantics_info(semantics_length=1))
    def test_add_variable_returns_a_different_integer_for_each_call(self, semantics_info1, semantics_info2):
        semantic_list1, semantic_type1, variable_name1 = semantics_info1
        semantic_list2, semantic_type2, variable_name2 = semantics_info2
        assume(len(variable_name1) > 0)
        assume(len(variable_name2) > 0)
        assume(semantic_list1 != semantic_list2)
        assume(variable_name1 != variable_name2)
        db = SemanticTrackerDB(semantics_length=1)
        semantics_id1 = db.add_variable(variable_name1, semantic_list1, semantic_type1)
        semantics_id2 = db.add_variable(variable_name2, semantic_list2, semantic_type2)
        assert semantics_id1 != semantics_id2