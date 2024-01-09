import os
from project_2_classes.my_token import Token
from project_2_classes.parser import Parser
from project1_classes.lexer_fsm import LexerFSM

def project2(input: str) -> str:

    lexer = LexerFSM()
    lexer.run(input)
    tokensWithComment = lexer.tokens
    tokens = []
    for token in tokensWithComment:
        if token.token_type != 'COMMENT':
            tokens.append(token)

    # this is our example list of tokens, for the actual project you will use the lexer to generate this
    
    parser = Parser()

    return parser.run(tokens)


def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read()


# Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("./project2-passoff/80/input0.txt")
    #os.chdir('.')
    #input_contents = "some string"
    print(project2(input_contents))
