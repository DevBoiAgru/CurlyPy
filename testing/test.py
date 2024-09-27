true = True; false = False
my_int: int = 5
my_float: float = 3.14
my_string: str = "Hello, World!"
my_bool: bool = True
my_dict: dict[str, int] = {"key1": 1, "key2": 2}
my_dict_with_types: dict = {"outer": {"inner": 1}}
empty_dict: dict = {}
my_set: set[int] = {1, 2, 3}
my_empty_set: set = {}
complex_type: dict = {"evens": {0, 2, 4}, "odds": {1, 3, 5}}
complex_dict: dict = {"numbers": [1, 2, 3]}
nested_dict: dict = {
"outer": {
"inner": 1,
"another_inner": {"key": 2}
}
}
if true :
    my_dict: dict[str, int] = {"a": 1, "b": 2}
    my_set: set[int] = {1, 2, 3}
else :
    my_other_dict: dict[str, str] = {"c": "3", "d": "4"}
comprehension_dict: dict[int, int] = {x: x*x for x in range(10)}
comprehension_set: set[int] = {x for x in range(10) if x % 2 == 0}
string_list_dict: dict = {
"list1": ["a", "b", "c"],
"list2": ["x", "y", "z"]
}
type_without_brackets: dict[str, int] = {"a": 1, "b": 2}
def my_function(param1: int, param2: dict) -> None:
    pass
def test_function() -> None :
    local_dict: dict[str, float] = {"pi": 3.14, "e": 2.71}
    local_set: set[str] = {"apple", "banana", "cherry"}
print("Hello, World!")