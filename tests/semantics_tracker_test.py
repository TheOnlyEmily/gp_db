from hypothesis import strategies as st, given
from gp_db.database import SemanticsTracker


semantics = lambda: st.lists(
    st.one_of(
        st.booleans(),
        st.floats(),
        st.text(),
    )
)

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
    assert st.get_semantics(sem_id) == semantics