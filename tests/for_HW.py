some_value = 'animal'
some_int = 123
some_value_2 = [1, 2, 3]

#def test_value_type():
#     assert isinstance(some_value_2, dict), f'ожидали что придет str, но пришло {type(some_value_2)}'

print(len(some_value_2))

def test_length():
    assert len(some_value) > 2  #can use for cases when youre testing the response you've received has info at all or not


