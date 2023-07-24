import pytest
from typing import Callable
from hypothesis import given, strategies as st, assume
from gp_db.database import SemanticTrackerDB

@st.composite
def semantics_info(draw: Callable, semantics_length=None) -> tuple[list, type]:
    semantics_type = draw(st.sampled_from([bool, int, str]))
    if semantics_length is not None:
        semantics_list = draw(st.lists(st.from_type(semantics_type), min_size=semantics_length, max_size=semantics_length))
    else:
        semantics_list = draw(st.lists(st.from_type(semantics_type), min_size=1))
    return semantics_list

class TestInitMethod:
    @given(st.integers())
    def test_constructor_takes_one_integer(self, semantics_length):
        assume(semantics_length > 0)
        
        SemanticTrackerDB(semantics_length)

    @given(st.integers())
    def test_constructor_raises_assertion_error_init_error_given_semantics_length_less_than_one(self, semantics_length):
        assume(semantics_length <= 0)

        with pytest.raises(AssertionError, match="semantics length must be postive and non-zero"): 
            SemanticTrackerDB(semantics_length)

    @given(st.one_of(st.booleans(), st.text(), st.floats()))
    def test_constructor_raises_assertion_error_given_semantics_length_not_of_type_int(self, semantics_length):
        with pytest.raises(AssertionError, match="semantics length must be of type integer"): 
            SemanticTrackerDB(semantics_length)


class TestAddVariableMethod:
    def test_add_variable_is_attribute(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert hasattr(db, "add_variable")

    def test_add_variable_is_callable(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert callable(db.add_variable)

    @given(semantics_info(semantics_length=1))
    def test_add_variable_takes_a_string_and_a_list(self, semantic_list):
        db = SemanticTrackerDB(semantics_length=1)
        db.add_variable(semantic_list)

    @given(semantic_list=st.one_of(st.booleans(), st.text(), st.floats()))
    def test_add_variable_raises_assertion_error_given_semantics_not_of_type_list(self, semantic_list):
        with pytest.raises(AssertionError, match="semantics must be of type list"):
            db = SemanticTrackerDB(semantics_length=1)
            db.add_variable(semantic_list)

    @given(semantics_info(), st.integers(min_value=1))
    def test_add_variable_raises_assertion_error_given_list_of_wrong_size(self, semantic_list, expected_length):
        assume(len(semantic_list) != expected_length)
        db = SemanticTrackerDB(semantics_length=expected_length)
        with pytest.raises(AssertionError, match=f"expected semantics of length {expected_length} not {len(semantic_list)}"):
            db.add_variable(semantic_list)

    @given(semantics_info(semantics_length=1))
    def test_add_variable_returns_an_integer(self, semantic_list):
        db = SemanticTrackerDB(semantics_length=1)
        semantics_id = db.add_variable(semantic_list)
        assert isinstance(semantics_id, int)

    @given(semantics_info(semantics_length=1), semantics_info(semantics_length=1))
    def test_add_variable_returns_a_different_integer_for_each_call(self, semantic_list1, semantic_list2):
        assume(semantic_list1 != semantic_list2)
        db = SemanticTrackerDB(semantics_length=1)
        semantics_id1 = db.add_variable(semantic_list1)
        semantics_id2 = db.add_variable(semantic_list2)
        assert semantics_id1 != semantics_id2


class TestAddFunctionMethod:

    def test_add_function_is_attribute(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert hasattr(db, "add_function")

    def test_add_function_is_callable(self):
        db = SemanticTrackerDB(semantics_length=1)
        assert callable(db.add_function)

    @given(func_name=st.text(min_size=1), func=st.functions())
    def test_add_function_takes_a_string_and_function(self, func_name, func):
        db = SemanticTrackerDB(semantics_length=1)
        db.add_function(func_name, func)
    
    @given(func_name=st.text(min_size=1), func=st.functions())
    def test_add_function_returns_none(self, func_name, func):
        db = SemanticTrackerDB(semantics_length=1)
        assert db.add_function(func_name, func) is None

    @given(func=st.functions())
    def test_add_function_raises_assertion_error_given_empty_string(self, func):
        func_name = ''
        db = SemanticTrackerDB(semantics_length=1)
        with pytest.raises(AssertionError, match="empty string is not a valid name"):
            db.add_function(func_name, func)

    @given(function_name=st.one_of(st.booleans(), st.floats()), func=st.functions())
    def test_add_function_raises_assertion_error_given_function_name_not_of_type_string(self, function_name, func):
        db = SemanticTrackerDB(semantics_length=1)
        with pytest.raises(AssertionError, match="name must be of type string"):
            db.add_function(function_name, func)

    @given(func_name=st.text(min_size=1), func=st.one_of(st.booleans(), st.text(), st.floats()))
    def test_add_function_raises_assertion_error_given_function_not_of_type_function(self, func_name, func):
        db = SemanticTrackerDB(semantics_length=1)
        with pytest.raises(AssertionError, match="function must be callable"):
            db.add_function(func_name, func)