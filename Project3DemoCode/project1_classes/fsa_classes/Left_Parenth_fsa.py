from .fsa import FSA
from typing import Callable

class LeftParenFSA(FSA):

    def __init__(self):
        self.num_read: int = 0
        self.new_lines_read: int = 0
        self.fsa_name = 'LEFT_PAREN'
    
    def s0(self, input)-> bool:
        #(don't need to return)
        #just make a variable
         if(input[0] == '('):
            self.num_read += 1
            return True
         else:
             return False