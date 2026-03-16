class Vehicle:
    def __init__(self, starting_top_speed = 100) -> None:
        self.top_speed = starting_top_speed
        self.__warnings = []

    def drive(self) -> None:
        print(f'I am driving but certainly not faster than {self.top_speed}')

    def add_warning(self, warning_text: str) -> None:
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)

    def get_warnings(self) -> list[str]:
        return self.__warnings

    def __repr__(self) -> str:
        return f'Top speed: {self.top_speed}, Warnings: {len(self.__warnings)}'
