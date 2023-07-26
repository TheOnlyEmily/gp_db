# Goal
Build a database for facilitating semantically driven genetic programming.

# Example Code
```python
from gp_db.database import SemanticTrackerDB

db = SemanticTrackerDB()

x_variable_id: int = db.add_semantics([0, 1, 0, 1])
y_variable_id: int = db.add_semantics([0, 0, 1, 1])

my_and = lambda a, b: a * b
my_not = lambda a: 1 - a
my_or = lambda a, b: a + b - a * b

not_x_variable_id: int = db.combine_semantics(my_not, [x_variable_id])
not_y_variable_id: int = db.combine_semantics(my_not, [y_variable_id])

x_and_not_y_id: int = db.combine_semantics(my_and, [x_variable_id, not_y_variable_id])
not_x_and_y_id: int = db.combine_semantics(my_and, [not_x_variable_id, y_variable_id])

x_xor_y_id: int = db.combine_semantics(my_or, [x_and_not_y_id, not_x_and_y_id])

print(db.get_semantics(x_xor_y_id)) # should print [0, 1, 1, 0]

ancestors: list[int] = db.get_ancestor_ids(x_xor_y_id)
assert len(ancestors) == 2
assert x_and_not_y_id in ancestors
assert not_x_and_y_id in ancestors
```