class Token():
    def __init__(self, token_type: str, value: str, line_num: int):
        self.token_type = token_type
        self.value = value
        self.line_num = line_num
        

    def to_string(self) -> str:
        return ("(" + f"{self.token_type}" + "," + '"' + f"{self.value}" + '"' + "," + f"{self.line_num}" + ")")
    