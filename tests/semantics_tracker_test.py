import numpy as np

from hypothesis import strategies as st, given, assume
from gp_db.tracker import SemanticsTracker


semantics = lambda: st.lists(
    st.one_of(
        st.booleans(),
        st.floats(allow_infinity=False, allow_nan=False),
        st.text(),
    )
).map(lambda v: np.array(v))

@given(semantics())
def test_add_semantics_takes_an_int_list_and_returns_an_int(semantics):
    st = SemanticsTracker()
    semantics_id: int = st.add_semantics(semantics)
    assert type(semantics_id) is int


@given(semantics(), semantics())
def test_add_semantics_returns_incrementing_ids(s1, s2):
    st = SemanticsTracker()
    sem_id1 = st.add_semantics(s1)
    sem_id2 = st.add_semantics(s2)
    assert sem_id2 == sem_id1 + 1

@given(semantics())
def test_get_semantics_retrieves_semantics_given_an_id(semantics):
    st = SemanticsTracker()
    sem_id = st.add_semantics(semantics)
    assert np.all(st.get_semantics(sem_id) == semantics)

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_combine_semantics_takes_two_semantics_ids_and_returns_semantic_id(sem1, sem2):
    st = SemanticsTracker()
    assume(len(sem1) == len(sem2))
    parent_id1 = st.add_semantics(sem1)
    parent_id2 = st.add_semantics(sem2)
    child_id = st.combine_semantics(np.add, [parent_id1, parent_id2])
    assert type(child_id) is int

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_combine_semantics_creates_new_semantics_using_from_function(sem1, sem2):
    st = SemanticsTracker()
    assume(len(sem1) == len(sem2))
    parent_id1 = st.add_semantics(sem1)
    parent_id2 = st.add_semantics(sem2)
    child_id = st.combine_semantics(np.add, [parent_id1, parent_id2])
    assert np.all(st.get_semantics(child_id) == np.add(sem1, sem2))

@given(st.lists(st.integers(), min_size=1))
def test_get_ancestor_graph_returns_one_node_for_semantics_added_through_add_semantics_method(sem):
    st = SemanticsTracker()
    sem_id = st.add_semantics(sem)
    ancestor_graph = st.get_ancestor_graph(sem_id)
    assert len(ancestor_graph) == 1
    assert sem_id in ancestor_graph