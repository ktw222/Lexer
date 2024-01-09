from .fsa import FSA
from typing import Callable

class SchemesFSA(FSA):

    def __init__(self):
        self.num_read: int = 0
        self.new_lines_read: int = 0
        self.fsa_name = 'SCHEMES'
    
    def s0(self, input)-> None:
         if(input[0] == 'S'):
            self.num_read += 1
            return self.s1(input[1:])
         
    def s1(self, input)-> None:
         if(input[0] == 'c'):
            self.num_read += 1
            return self.s2(input[1:])
         
    def s2(self, input)-> None:
         if(input[0] == 'h'):
            self.num_read += 1
            return self.s3(input[1:])
         
    def s3(self, input)-> None:
         if(input[0] == 'e'):
            self.num_read += 1
            return self.s4(input[1:])
         
    def s4(self, input)-> None:
         if(input[0] == 'm'):
            self.num_read += 1
            return self.s5(input[1:])
         
    def s5(self, input)-> None:
         if(input[0] == 'e'):
            self.num_read += 1
            return self.s6(input[1:])
         
    def s6(self, input) -> bool:
        if(not input):
            self.num_read = 0
            return False
        if (input [0] == 's'):
            self.num_read += 1
            return True
        


    