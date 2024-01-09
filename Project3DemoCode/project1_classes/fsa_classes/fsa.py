from typing import Callable

class FSA:
    
    def __init__(self):
        self.num_read = 0
        self.new_lines_read = 0

    
    #def s0(self, input_string) -> Callable:
        #raise NotImplementedError()
    
    
    def run(self, input_string: str) -> bool:
        self.reset()
        return self.s0(input_string)

    def reset(self) -> None:
        self.num_read = 0
        self.new_lines_read = 0

    def get_name(self) -> str: 
        return self.fsa_name

    def set_name(self, FSA_name) -> None:
        self.fsa_name = FSA_name

    def get_new_lines_read(self) -> int:
        return self.new_lines_read

    def get_num_read(self) -> int:
        return self.num_read

    def __get_current_input(self) -> str:  # The double underscore makes the method private
        return self.input_string