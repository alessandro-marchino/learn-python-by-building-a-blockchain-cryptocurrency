# 1) Create a list of names and use a for loop to output the length of each name (len() ).
names = [ 'Max', 'Luke', 'Maria', 'Frederick', 'Maximilian', 'Nicholas' ]
for name in names:
    print(f'Name {name} is {len(name)} long')
print('-' * 20)

# 2) Add an if  check inside the loop to only output names longer than 5 characters.
for name in names:
    if len(name) > 5:
        print(f'Name {name} is {len(name)} long')
print('-' * 20)

# 3) Add another if  check to see whether a name includes a “n”  or “N”  character.
for name in names:
    if len(name) > 5 and ('n' in name or 'N' in name):
        print(f'Name {name} is {len(name)} long and contains \'n\' or \'N\'')
print('-' * 20)
# 4) Use a while loop to empty the list of names (via pop())
while len(names) > 0:
    print(f'Removed name {names.pop()}')
print(names)

print('-' * 20)
