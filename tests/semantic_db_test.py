from hypothesis import given, strategies as st, assume
from gp_db.database import SemanticTrackerDB


def test_constructor_takes_no_arguments():
    SemanticTrackerDB()


class TestAddVariableMethod:
    def test_add_variable_is_attribute(self):
        db = SemanticTrackerDB()
        assert hasattr(db, "add_variable")

    def test_add_variable_is_callable(self):
        db = SemanticTrackerDB()
        assert callable(db.add_variable)

    @given(st.text(), st.lists(st.one_of(st.booleans(), st.integers(), st.text())))
    def test_add_variable_takes_a_string_and_a_list(self, variable_name, semantic_list):
        assume(len(variable_name) > 0)
        assume(len(semantic_list) > 0)
        db = SemanticTrackerDB()
        db.add_variable(variable_name, semantic_list)

    @given(st.text(), st.lists(st.one_of(st.booleans(), st.integers(), st.text())))
    def test_add_variable_returns_an_integer(self, variable_name, semantic_list):
        assume(len(variable_name) > 0)
        assume(len(semantic_list) > 0)
        db = SemanticTrackerDB()
        semantics_id = db.add_variable(variable_name, semantic_list)
        assert isinstance(semantics_id, int)