# 1) Import the random function and generate both a random number between 0 and 1 as well as a random number between 1 and 10.
import random

print(f'Random number between 0 and 1: {random.random()}')
print(f'Random number between 1 and 10: {random.randint(1, 10)}')

# 2) Use the datetime library together with the random number to generate a random, unique value.
import datetime

date = datetime.datetime.now()
print(f'Random value with date: {random.random()} - {date}')
