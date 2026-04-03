# 1) Create a Food class with a "name" and a "kind" attribute as well as a
#    "describe()"" method (which prints "name" and "kind" in a sentence).
class Food:
    name = 'X'
    kind = 'Y'

    def __init__(self, name: str, kind: str) -> None:
        self.name = name
        self.kind = kind

    def describe(self) -> None:
        print(f"""I am a {self.__class__.__name__}.
              My name is {self.name} and my kind is {self.kind}""")

    # 2) Try turning describe() from an instance method into a class and a
    #    static method. Change it back to an instance method thereafter.
    @classmethod
    def describe2(cls) -> None:
        print(f"""I am a Food.
              My name is {cls.name} and my kind is {cls.kind}""")

    @staticmethod
    def describe3() -> None:
        print(f"""I am a Food.
              My name is {Food.name} and my kind is {Food.kind}""")

# 4) Overwrite a "dunder" method to be able to print your "Food" class.
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} == {str(self.__dict__)}'


# 3) Create a "Meat" and a "Fruit" class – both should inherit from "Food".
#    Add a "cook()" method to "Meat" and "clean()" to "Fruit.
class Meat(Food):
    def __init__(self, name: str) -> None:
        super().__init__(name, 'Meat')

    def cook(self) -> None:
        print('Cooking...')


class Fruit(Food):
    def __init__(self, name: str) -> None:
        super().__init__(name, 'Fruit')

    def clean(self) -> None:
        print('Clenaing...')


food = Food('Margherita', 'Pizza')
food.describe()
Food.describe2()
Food.describe3()
print(food)

meat = Meat('Steak')
meat.describe()
meat.cook()
print(meat)

fruit = Fruit('Banana')
fruit.describe()
fruit.clean()
print(fruit)
