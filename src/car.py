class Car:
    def __init__(self, starting_top_speed = 100) -> None:
        self.top_speed = starting_top_speed
        self.warnings = []

    def drive(self) -> None:
        print(f'I am driving but certainly not faster than {self.top_speed}')

car1 = Car()
car1.drive()
car1.warnings.append('New warning')

car2 = Car(200)
car2.drive()

car3 = Car(250)
car3.drive()
