from vehicle import Vehicle

class Car(Vehicle):
    def brag(self) -> None:
        print('Look how cool my car is')


car1 = Car()
car1.drive()
car1.add_warning('New warning')
car1.add_warning('')
# print(car1.__dict__)
print(car1)

car2 = Car(200)
car2.drive()
print(car2)

car3 = Car(250)
car3.drive()
print(car3)
print(car3.get_warnings())
