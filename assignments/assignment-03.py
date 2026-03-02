# 1) Create a list of "person" dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.
persons = [
    { 'name': 'Max', 'age': 30, 'hobbies': [ 'Programming', 'Reading' ] },
    { 'name': 'Luke', 'age': 45, 'hobbies': [ 'Reading', 'Movies' ] },
    { 'name': 'Anna', 'age': 18, 'hobbies': [ 'Dancing', 'Skating' ] },
]
print(persons)

# 2) Use a list comprehension to convert this list of persons into a list of names (of the persons).
names = [ el['name'] for el in persons ]
print(names)

# 3) Use a list comprehension to check whether all persons are older than 20.
all_over_20 = all([ el['age'] > 20 for el in persons ])
print(all_over_20)

# 4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).
new_list = [ el.copy() for el in persons ]
new_list[0]['name'] = 'Eddie'
print(new_list)

# 5) Unpack the persons of the original list into different variables and output these variables.
p1, p2, p3 = persons
print(p1)
print(p2)
print(p3)
