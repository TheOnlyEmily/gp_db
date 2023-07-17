# Goal
Build a database for facilitating semantically driven genetic programming.

# Example Code
```python
from gp_db.database import SemanticDB

db = SemanticDB()

x_variable_id: int = db.add_variable(name='x', value=[0, 1, 0, 1])
y_variable_id: int = db.add_variable(name='y', value=[0, 0, 1, 1])

not_function_id: int = db.add_function(name="not", function=lambda v: int(not v), arg_types=[int], output_type=int)
and_function_id: int = db.add_function(name="and", function=lambda a, b: int(a and b), arg_types=[int, int], output_type=int)
or_function_id: int = db.add_function(name="or", function=lambda a, b: int(a or b), arg_types=[int, int], output_type=int)

not_x_variable_id: int = db.combine_semantics(function=not_function_id, arguments=[x_variable_id])
not_y_variable_id: int = db.combine_semantics(function=not_function_id, arguments=[y_variable_id])

x_and_not_y_id: int = db.combine_semantics(function=and_function_id, arguments=[x_variable_id, not_y_variable_id])
not_x_and_y_id: int = db.combine_semantics(function=and_function_id, arguments=[not_x_variable_id, y_variable_id])

x_xor_y_id: int = db.combine_semantics(function=or_function_id, arguments=[x_and_not_y_id, not_x_and_y_id])

print(db.get_semantics(x_xor_y_id)) # should print [0, 1, 1, 0]

left_id, right_id = db.get_first_decendant_ids(x_xor_y_id)
assert left_id == x_and_not_y_id # should pass
assert right_id == not_x_and_y_id # should pass
```