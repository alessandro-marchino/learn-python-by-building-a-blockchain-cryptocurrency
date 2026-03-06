# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.
def normal_function(fnc):
    print(fnc())

# 2) Call your “normal” function by passing a lambda function - which performs any operation of your choice - as an argument.
normal_function(lambda: 42)

# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.
def normal_function2(fnc, *args):
    print(fnc(*args))

normal_function2(lambda a, b: a + b, 1, 2)
normal_function2(lambda a, b, c, d, e: a + b + c + d + e, 1, 2, 3, 4, 5)

# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.
def normal_function3(fnc, *args):
    print(f'Result: {fnc(*args):20.2f}')
normal_function3(lambda a, b, c, d, e: a + b + c + d + e, 1, 2, 3, 4, 5)
