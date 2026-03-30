class NetworkError(Exception):
    def __init__(self, msg:str, status_code:int, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg
        self.status_code = status_code
