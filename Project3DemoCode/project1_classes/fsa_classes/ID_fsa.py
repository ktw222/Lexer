from .fsa import FSA
from typing import Callable

class IdFSA(FSA):

    def __init__(self):
        self.num_read: int = 0
        self.new_lines_read: int = 0
        self.fsa_name = 'ID'
    
    def s0(self, input)-> None:
         if(input[0].isalpha()):
            self.num_read += 1
            return self.s1(input[1:])

    def s1(self, input) -> None:
        if(not input):
            self.num_read = 0
            return False
        if (input [0].isalnum()):
            self.num_read += 1
            return self.s1(input[1:])
        else: return True
        
        