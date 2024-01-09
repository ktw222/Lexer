from .fsa_classes.fsa import FSA
from .fsa_classes.colon_fsa import ColonFSA
from .fsa_classes.colon_dash_fsa import ColonDashFSA
from .fsa_classes.Comma_fsa import CommaFSA
from .fsa_classes.Left_Parenth_fsa import LeftParenFSA
from .fsa_classes.Multiply_fsa import MultiplyFSA
from .fsa_classes.Period_fsa import PeriodFSA
from .fsa_classes.Plus_fsa import AddFSA
from .fsa_classes.Q_Mark_fsa import Q_MarkFSA
from .fsa_classes.Right_Parenth_fsa import RightParenFSA
from .fsa_classes.Schemes_fsa import SchemesFSA
from .fsa_classes.Queries_fsa import QueriesFSA
from .fsa_classes.Rules_fsa import RulesFSA
from .fsa_classes.Facts_fsa import FactsFSA
from .fsa_classes.ID_fsa import IdFSA
from .fsa_classes.Comment_FSA import CommentFSA
from .fsa_classes.String_fsa import StringFSA
from .token import Token

class LexerFSM:
    def __init__(self):
        self.tokens: list[Token] = []
        self.automota: list[FSA] = []
        self.colon_fsa: ColonFSA = ColonFSA()
        self.colon_dash_fsa: ColonDashFSA = ColonDashFSA()
        self.Comma_fsa: CommaFSA = CommaFSA()
        self.Left_Parenth_fsa: LeftParenFSA = LeftParenFSA()
        self.Multiply_fsa: MultiplyFSA = MultiplyFSA()
        self.Period_fsa: PeriodFSA = PeriodFSA()
        self.Plus_fsa: AddFSA = AddFSA()
        self.Q_Mark_fsa: Q_MarkFSA = Q_MarkFSA()
        self.Right_Parenth_fsa: RightParenFSA = RightParenFSA()
        self.Schemes_fsa: SchemesFSA = SchemesFSA()
        self.Queries_fsa: QueriesFSA = QueriesFSA()
        self.Rules_fsa: RulesFSA = RulesFSA()
        self.Facts_fsa: FactsFSA = FactsFSA()
        self.ID_fsa: IdFSA = IdFSA()
        self.Comment_FSA: CommentFSA = CommentFSA()
        self.String_fsa: StringFSA = StringFSA()


        self.line_num: int = 1
        self.automota.append(self.Comma_fsa)
        self.automota.append(self.colon_fsa)
        self.automota.append(self.colon_dash_fsa)
        self.automota.append(self.Left_Parenth_fsa)
        self.automota.append(self.Multiply_fsa)
        self.automota.append(self.Period_fsa)
        self.automota.append(self.Plus_fsa)
        self.automota.append(self.Q_Mark_fsa)
        self.automota.append(self.Right_Parenth_fsa)
        self.automota.append(self.Schemes_fsa)
        self.automota.append(self.Queries_fsa)
        self.automota.append(self.Rules_fsa)
        self.automota.append(self.Facts_fsa)
        self.automota.append(self.ID_fsa)
        self.automota.append(self.Comment_FSA)
        self.automota.append(self.String_fsa)
        # other FSA classes and any other member variables you need
    
    
    def run(self, input: str) -> str:
        
        #line_num: int = 1
        while (input):
            max_read: int = 0
            max_automoton: FSA = None
            #num_tokens: 
            if (input[0].isspace()):
                if (input[0] == '\n'): self.line_num += 1
                input = input[1:]
                continue
            
    
            for automoton in self.automota:
                DidAccept = automoton.run(input)

                num_read: int = automoton.get_num_read() #make exception state for false
                if (DidAccept):
                    if (num_read > max_read):
                        max_read = num_read
                        max_automoton = automoton
            if(max_automoton is not None):
                token = Token(max_automoton.get_name(),input[0:max_read],self.line_num)
                self.tokens.append(token)
                #num_tokens += 1
                #print(self.tokens)
                #create the token associated with the max automaton
                #print(token.to_string())
                #added self.input instead of input
                input = input[max_read:]
                self.line_num += max_automoton.get_new_lines_read()
            else:
                token = Token("UNDEFINED", input[0], self.line_num)
                self.tokens.append(token)
                max_read = 1
                input = input[max_read:]
                string_of_tokens = ""
                for token in self.tokens:
                    string_of_tokens += (token.to_string()) + "\n"
                return string_of_tokens + f"\nTotal Tokens = Error on line {self.line_num}\n"
                #print(token.to_string())
                #break
            
        token = Token('EOF',"",self.line_num)
        self.tokens.append(token)
        #print(token.to_string())
        string_of_tokens = ""
        for token in self.tokens:
            string_of_tokens += (token.to_string()) + "\n"
        return string_of_tokens + f"Total Tokens = {len(self.tokens)}\n"
        


#create EOF token


    def lex(self, input_string: str) -> Token:
        ...

    def __manager_fsm__(self) -> Token:
        ...

    def reset(self) -> None:
        ...