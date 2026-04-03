# 1) Create two variables – one with your name and one with your age
name = 'Alessandro'
age = 37


# 2) Create a function which prints your data as one string
def print_data() -> None:
    print(f'Name: {name} - Age: {age}')


print_data()


# 3) Create a function which prints ANY data (two arguments) as one string
def print_args(arg1: object, arg2: object) -> None:
    print(f'{arg1} - {arg2}')


print_args(age, name)


# 4) Create a function which calculates and returns the number of decades you
#    already lived (e.g. 23 = 2 decades)
def compute_decades() -> int:
    return age // 10


print(compute_decades())
