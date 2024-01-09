from .fsa import FSA
from typing import Callable

class CommentFSA(FSA):

    def __init__(self):
        self.num_read: int = 0
        self.new_lines_read: int = 0
        self.fsa_name = 'COMMENT'
    
    def s0(self, input)-> None:
        #(don't need to return)
        #just make a variable
         if(input[0] == '#'):
            self.num_read += 1
            return self.S1(input[1:])

    def S1(self, input) -> None:
        if(not input):
            self.num_read = 0
            return False
        if (input [0] != '\n'):
            self.num_read += 1
            return self.S1(input[1:])
        else: return True
        