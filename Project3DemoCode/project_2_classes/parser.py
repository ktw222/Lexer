from Project3DemoCode.project_2_classes.my_token import Token

class Predicate():
    def __init__(self, name: str, parameters: list[str]):
        self.name = name
        self.parameters: list[str] = parameters
    
    def to_string(self):
        param_str: str = ""
        param_str = ','.join(self.parameters)
        return(f'{self.name}({param_str})')
    
    #datalog
    #list of schemes and list of facts which ocntains predicates
    # define to string _> lab description (use lab description to determine)
    #in run create datalog program and them parse the datalog program

class DatalogProgram():
    def __init__(self):
        self.scheme_list: list[Predicate] = [] #list of predicates
        self.fact_list: list[Predicate] = [] #list of predicates
        self.query_list: list[Predicate] = [] #list of predicates
        self.rule_list: list[Rules] = [] #list of rules
        self.domain: set[str] = set() #all parameters in facts

    def sortDomain(self):
        self.domain = sorted(self.domain)
        return self.domain

    def to_string(self):
        
        schemeLen = len(self.scheme_list)
        factLen = len(self.fact_list)
        queryLen = len(self.query_list)
        ruleLen = len(self.rule_list)
        domainLen = len(self.domain)

        schemesString = f'Schemes({schemeLen}):\n'
        for schemeVal in self.scheme_list:
            schemesString += f"  {schemeVal.to_string()}\n"

        factString = f'Facts({factLen}):\n'
        for factVal in self.fact_list:
            factString += f"  {factVal.to_string()}.\n"
        
        ruleString = f'Rules({ruleLen}):\n'
        for ruleVal in self.rule_list:
            ruleString += f"  {ruleVal.to_string()}\n"

        queryString = f'Queries({queryLen}):\n'
        for queryVal in self.query_list:
            queryString += f"  {queryVal.to_string()}?\n"

        domainString = f'Domain({domainLen}):\n'
        sortedString = self.sortDomain()
        for domainVal in sortedString:
            domainString += f"  {domainVal}\n"

        datalogString = schemesString + factString + ruleString + queryString + domainString
        
        return datalogString
    
    #add to domain -> self.datalogprogram.schemes/facts/queries/domain/etc
        
#class Parameter():
    #def __init__(self, name):
        #self.name = name
    #def to_string(self):
        #return self.name

class Rules():#update head predicate :- list of predicates
    def __init__(self, head_predicate, rule_list):
        self.head_predicate = head_predicate
        self.rule_list = rule_list

    def to_string(self):

        rule_str = f'{self.head_predicate.to_string()} :- {",".join(predicate.to_string() for predicate in self.rule_list)}.'
        return rule_str

class Parser():
    def __init__(self):
        self.datalogProgram = DatalogProgram()


    def throw_error(self):
        raise ValueError(self.get_curr_token().to_string())

    def get_curr_token(self) -> Token:
        if (self.index >= len(self.tokens)):
            self.index = len(self.tokens) - 1
            self.throw_error()
        return self.tokens[self.index]
    
    def get_prev_token_value(self) -> str:
        return self.tokens[self.index - 1].value
    
    def advance(self):
        self.index += 1

    def match(self, expected_type: str):
        if(self.get_curr_token().token_type == expected_type):
            self.advance()
        else:
            self.throw_error()

    def run(self, tokens: list[Token]) -> str:
        self.index: int = 0
        self.tokens: list[Token] = tokens

        try:
            scheme: Predicate = self.parse_datalogProgram() #going to use self.parse_datalog_program() in the end
            return self.datalogProgram
        except ValueError as err:
            return f"Failure!\n  {err}"
        
    

    # scheme   	-> 	ID LEFT_PAREN ID idList RIGHT_PAREN
    def parse_scheme(self) -> Predicate:
        name = ""
        parameters: list[str] = []
        self.match("ID")
        name = self.get_prev_token_value()

        self.match("LEFT_PAREN")
        self.match("ID")
        parameters.append(self.get_prev_token_value())
        parameters += self.parse_id_list()

        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)
    
    # idList  	-> 	COMMA ID idList | lambda
    def parse_id_list(self) -> list[str]:
        #first production
        #the first set is {COMMA}
        if (self.get_curr_token().token_type == "COMMA"):
            self.match("COMMA")
            self.match("ID")
            curr_id: list[str] = [self.get_prev_token_value()]
            #[name]
            rest_of_ids: list[str] = self.parse_id_list()
            #[Address, PhoneNumber]
            #expected output -> [name, Address, PhoneNumber]
            return curr_id + rest_of_ids

        #lambda
        else:
            return []
    # stringList    ->    COMMA STRING stringList   |   lambda
    def parse_string_list(self) -> list[str]:
        if (self.get_curr_token().token_type == "COMMA"):
            self.match("COMMA")
            self.match("STRING")
            curr_id: list[str] = [self.get_prev_token_value()]
            rest_of_ids: list[str] = self.parse_string_list()
            return curr_id + rest_of_ids
        
        else:
            return []
    # parameterList    ->    COMMA parameter parameterList   |   lambda    
    def parse_parameter_list(self) -> list[str]:
        if (self.get_curr_token().token_type == "COMMA"):
            self.match("COMMA")
            #parameter
            self.parse_parameter()
            #parameter list
            curr_id: list[str] = [self.get_prev_token_value()]
            rest_of_ids: list[str] = self.parse_parameter_list()
            return curr_id + rest_of_ids

        else:
            return []
    # parameter  ->  STRING  |  ID       
    def parse_parameter(self) -> str:
        name = ""
        if (self.get_curr_token().token_type == "STRING"):
            self.match("STRING")
            name = self.get_prev_token_value()
            return name
        if (self.get_curr_token().token_type == "ID"):
            self.match("ID")
            name = self.get_prev_token_value()
            return name
        raise ValueError("Expected COMMA or ID for parameter, but found: " + self.get_curr_token().to_string())
    # predicateList  ->  COMMA predicate predicateList  |  lambda
    def parse_predicate_list(self) -> list[Predicate]:#take in rule and add predicates to rule rest list
        parameters: list[Predicate] = []
        if (self.get_curr_token().token_type == "COMMA"):
            self.match("COMMA")
            parameters.append(self.parse_predicate())
            #parameters += self.parse_predicate()
            parameters += self.parse_predicate_list()

            return parameters

        else:
            return []
    # predicate -> ID LEFT_PAREN parameter parameterList RIGHT_PAREN
    def parse_predicate(self) -> Predicate:#predicate
        name = ""
        parameters: list[str] = []
        self.match("ID")
        #print(self.match("ID"))
        name = self.get_prev_token_value()
        #print(name)

        self.match("LEFT_PAREN")
        #print(self.match("LEFT_PAREN"))
        
        #parameters.append(self.get_prev_token_value())
        parameters.append(self.parse_parameter())

        #parameters.append(self.get_prev_token_value())
        parameters += self.parse_parameter_list()

        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)


    #headPredicate  ->  ID LEFT_PAREN ID idList RIGHT_PAREN
    def parse_head_predicate(self) -> Predicate:#predicate

        name = ""
        parameters: list[str] = []
        self.match("ID")
        #print(self.match("ID"))
        name = self.get_prev_token_value()
        #print(name)

        self.match("LEFT_PAREN")
        #print(self.match("LEFT_PAREN"))

        self.match("ID")
        
        parameters.append(self.get_prev_token_value())
        parameters += self.parse_id_list()

        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)

    # query  ->  predicate Q_MARK
    def parse_query(self) -> Predicate:
        predicate_for_query = self.parse_predicate()
        self.match("Q_MARK")
        return predicate_for_query

    # rule  ->	headPredicate COLON_DASH predicate predicateList PERIOD
    def parse_rule(self) -> Rules: #return rule object add a head predicate first
        
        curr_head_predicate = self.parse_head_predicate()
        #currRule.head_predicate = curr_head_predicate

        self.match("COLON_DASH")

        curr_list_of_rules = []

        curr_predicate = self.parse_predicate()
        curr_list_of_rules.append(curr_predicate)

        curr_list_of_rules += self.parse_predicate_list()

        #currRule.rule_list = curr_list_of_rules
        currRule = Rules(curr_head_predicate, curr_list_of_rules)

        self.match("PERIOD")

        return currRule

    # fact ->	ID LEFT_PAREN STRING stringList RIGHT_PAREN PERIOD
    def parse_fact(self) -> Predicate:
        name = ""
        parameters: list[str] = []
        
        self.match("ID")
        #print(self.match("ID"))
        name = self.get_prev_token_value()
        #print(name)

        self.match("LEFT_PAREN")
        #print(self.match("LEFT_PAREN"))

        self.match("STRING")

        parameters.append(self.get_prev_token_value())
        parameters += self.parse_string_list()

        self.match("RIGHT_PAREN")
        self.match("PERIOD")
        for currParam in parameters:
            self.datalogProgram.domain.add(currParam)
        return Predicate(name, parameters)

    # datalogProgram	->	SCHEMES COLON scheme schemeList FACTS COLON factList RULES COLON ruleList QUERIES COLON query queryList EOF
    def parse_datalogProgram(self) -> list[str]:
        self.datalogProgram = DatalogProgram() 

        self.match("SCHEMES")
        self.match("COLON")
        myScheme = self.parse_scheme()
        self.datalogProgram.scheme_list.append(myScheme)
        self.parse_schemeList(self.datalogProgram.scheme_list)

        self.match("FACTS")
        self.match("COLON")
        if (self.get_curr_token().token_type == "ID"):
            myFact = self.parse_fact()
            self.datalogProgram.fact_list.append(myFact)
            self.parse_factList(self.datalogProgram.fact_list) 

        self.match("RULES")
        self.match("COLON")
        if (self.get_curr_token().token_type == "COLON_DASH" or self.get_curr_token().token_type == "ID"):
            myRule = self.parse_rule()
            self.datalogProgram.rule_list.append(myRule)
            self.parse_ruleList(self.datalogProgram.rule_list) 

        self.match("QUERIES")
        self.match("COLON")
        myQuery = self.parse_query()
        self.datalogProgram.query_list.append(myQuery)
        self.parse_queryList(self.datalogProgram.query_list)

        self.match("EOF")

        return self.datalogProgram

    # schemeList	->	scheme schemeList | lambda
    def parse_schemeList(self, scheme_list: list[Predicate]) -> list[str]: 
        # FIRST(schemeList recursion) = {ID} 
        if self.get_curr_token().token_type == "ID": 
            scheme_list.append(self.parse_scheme())
            # scheme 
            #self.parse_scheme
            # schemeList 
            self.parse_schemeList(scheme_list) 
            # FOLLOW(schemeList recursion) = {FACTS} 
        elif self.get_curr_token().token_type == "FACTS": 
            # Terminate tail recursion on token in follow set 
            return
        else:# error 
            raise ValueError(self.get_curr_token().to_string())


    # factList	->	fact factList | lambda
    def parse_factList(self, fact_list: list[Predicate]) -> list[str]:
        # FIRST(schemeList recursion) = {ID} 
        if self.get_curr_token().token_type == "ID": 
            fact_list.append(self.parse_fact())
            # scheme 
            #self.parse_fact() 
            # schemeList 
            self.parse_factList(fact_list) 
            # FOLLOW(factList recursion) = {RULES} 
        elif self.get_curr_token().token_type == "RULES": 
            # Terminate tail recursion on token in follow set 
            return
        else:# error 
            raise ValueError(self.get_curr_token().to_string())
        

    # ruleList	->	rule ruleList | lambda
    def parse_ruleList(self, rule_list: list[Predicate]) -> list[str]:
        # FIRST(ruleList recursion) = {ID} 
        if self.get_curr_token().token_type == "ID": 
            rule_list.append(self.parse_rule())
            # scheme 
            #self.parse_rule() 
            # schemeList 
            self.parse_ruleList(rule_list) 
            # FOLLOW(factList recursion) = {QUERIES} 
        elif self.get_curr_token().token_type == "QUERIES": 
            # Terminate tail recursion on token in follow set 
            return
        else:# error 
            raise ValueError(self.get_curr_token().to_string)
    # queryList	->	query queryList | lambda
    def parse_queryList(self, query_list: list[Predicate]) -> list[str]: 
        # FIRST(queryList recursion) = {ID} 
        if self.get_curr_token().token_type == "ID": 
            query_list.append(self.parse_query())
            # scheme 
            #self.parse_query() 
            # schemeList 
            self.parse_queryList(query_list) 
            # FOLLOW(factList recursion) = {EOF} 
        elif self.get_curr_token().token_type == "EOF": 
            # Terminate tail recursion on token in follow set 
            return
        else:# error 
            raise ValueError(self.get_curr_token().to_string())




        
        #implement rest of production functions
        #2 test
        #3 make a datalog program class
        #4 populate datalog program class


    