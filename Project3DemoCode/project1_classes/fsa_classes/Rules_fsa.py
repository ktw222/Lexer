from .fsa import FSA
from typing import Callable

class RulesFSA(FSA):

    def __init__(self):
        self.num_read: int = 0
        self.new_lines_read: int = 0
        self.fsa_name = 'RULES'
    
    def s0(self, input)-> None:
        #(don't need to return)
        #just make a variable
         if(input[0] == 'R'):
            self.num_read += 1
            return self.s1(input[1:])
    def s1(self, input)-> None:
        #(don't need to return)
        #just make a variable
         if(input[0] == 'u'):
            self.num_read += 1
            return self.s2(input[1:])
    def s2(self, input)-> None:
        #(don't need to return)
        #just make a variable
         if(input[0] == 'l'):
            self.num_read += 1
            return self.s3(input[1:])
    def s3(self, input)-> None:
        #(don't need to return)
        #just make a variable
         if(input[0] == 'e'):
            self.num_read += 1
            return self.s4(input[1:])
    
    def s4(self, input) -> bool:
        if(not input):
            self.num_read = 0
            return False
        if (input [0] == 's'):
            self.num_read += 1
            return True
        


    