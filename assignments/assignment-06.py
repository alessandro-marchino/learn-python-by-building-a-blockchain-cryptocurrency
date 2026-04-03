import json
import pickle


# 1) Write a short Python script which queries the user for input (infinite
#    loop with exit possibility) and writes the input to a file.
def objective1():
    while True:
        print('Give an input (q to exit): ')
        user_input = input()
        if user_input == 'q':
            break
        with open('assignment-06-1.txt', 'a') as f:
            f.write(f'{user_input}\n')


# 2) Add another option to your user interface: The user should be able to
#     output the data stored in the file in the terminal.
def objective2():
    while True:
        print('Give an input: ')
        print('(q to exit)')
        print('(s to spool to terminal)')
        user_input = input('Your input: ')
        if user_input == 'q':
            break
        elif user_input == 's':
            with open('assignment-06-2.txt', 'r') as f:
                print(f.read())
        else:
            with open('assignment-06-2.txt', 'a') as f:
                f.write(f'{user_input}\n')


# 3) Store user input in a list (instead of directly adding it to the file)
#    and write that list to the file – both with pickle and json.
def objective3():
    data = []
    while True:
        print('Give an input: ')
        print('(q to exit)')
        print('(s to spool to terminal)')
        user_input = input('Your input: ')
        if user_input == 'q':
            break
        elif user_input == 's':
            print(str(data))
        else:
            data.append(user_input)
            with open('assignment-06-3.json', 'w') as f:
                f.write(json.dumps(data))
            with open('assignment-06-3.pickle', 'wb') as f:
                f.write(pickle.dumps(data))


# 4) Adjust the logic to load the file content to work with pickled/ json data.
def objective4():
    with open('assignment-06-3.json', 'r') as f:
        data_json = json.loads(f.read())
    with open('assignment-06-3.pickle', 'rb') as f:
        data_pickle = pickle.loads(f.read())

    while True:
        print('Give an input: ')
        print('(q to exit)')
        print('(s to spool to terminal)')
        user_input = input('Your input: ')
        if user_input == 'q':
            break
        elif user_input == 's':
            print(str(data_json))
        else:
            data_json.append(user_input)
            data_pickle.append(user_input)
            with open('assignment-06-3.json', 'w') as f:
                f.write(json.dumps(data_json))
            with open('assignment-06-3.pickle', 'wb') as f:
                f.write(pickle.dumps(data_pickle))


objective4()
