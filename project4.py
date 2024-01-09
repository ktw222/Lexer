#Return your program output here for grading (can treat this function as your "main")
from Project3DemoCode.project_2_classes.parser import Parser
from Project3DemoCode.project1_classes.lexer_fsm import LexerFSM
from Project3DemoCode.project1_classes.token import Token
from Project3DemoCode.Interpreter import Interpreter
from Project3DemoCode.project_2_classes.parser import DatalogProgram
from Project3DemoCode.Relation import Relation
def project4(input: str) -> str:
    lexer = LexerFSM()
    lexer.run(input)
    tokensWithComment = lexer.tokens
    tokens = []
    for token in tokensWithComment:
        if token.token_type != 'COMMENT':
            tokens.append(token)

    # this is our example list of tokens, for the actual project you will use the lexer to generate this
    
    parser = Parser()
    datalog_program = parser.run(tokens)
    interpreter = Interpreter()

    return interpreter.run(datalog_program)

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents(r"C:\Users\ktwil\OneDrive\Documents\CS 236\project-4-ktw222-main\project-4-ktw222-main\project4-passoff\80\input0.txt")
    print(project4(input_contents))
