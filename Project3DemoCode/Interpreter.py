from .Relation import Relation
from .Row import Row
from .Header import Header
from typing import Dict
from Project3DemoCode.project_2_classes.parser import DatalogProgram
from Project3DemoCode.project_2_classes.parser import Predicate
from Project3DemoCode.project_2_classes.parser import Rules
from Project3DemoCode.Graph import Graph
import copy
# remove this and delete the file 
# after you add in your code from project 2
#from class_stubs import * 

class Interpreter:
    def __init__(self) -> None:
        self.output_str: str = ""
        self.database: Dict[str, Relation] = {}
        pass
    
    def run(self, datalog_program: DatalogProgram) -> str:
        self.datalog_program: DatalogProgram = datalog_program
        self.interpret_schemes()
        self.interpret_facts()
        self.interpret_rules()
        self.interpret_queries()
        return self.output_str #append to self.output_str rather than printing to console
    
    def interpret_schemes(self) -> None:
        # Start with an empty Database. 
        #for Schemes in DatalogProgram:
        for scheme in self.datalog_program.scheme_list:
            relation_name = scheme.name
            header = Header(scheme.parameters)
            new_relation = Relation(relation_name, header, set())
            self.database[scheme.name] = new_relation

     
    
    def interpret_facts(self) -> None:
        # For each fact in the Datalog program, 
        for fact in self.datalog_program.fact_list:
            row : Row
            row = Row(fact.parameters)
            if fact.name in self.database.keys():
        #   add a Tuple to a Relation. //in database
                self.database[fact.name].add_row(row)
        

    
    def interpret_queries(self) -> None:
        #print("queries")
        self.output_str += f"\nQuery Evaluation\n"
        for query in self.datalog_program.query_list:
            evaluated_query = self.evaluate_predicate(query)
            self.output_str += f"{query.to_string()}? "
            if len(evaluated_query.rows) == 0:
                self.output_str += "No\n"
            else:
                self.output_str += f"Yes({len(evaluated_query.rows)})\n"
                #maybe put an if statement here?
                for row in sorted(evaluated_query.rows):
                    self.output_str += "  "
                    for i in range(len(evaluated_query.header.values)): #header range
                        #attribute = evaluated_query.header.values[i]
                        value = row.values[i]
                        query_attribute = evaluated_query.header.values[i]

                        self.output_str += f"{query_attribute}={value}, "
                    self.output_str = self.output_str[:-2]
                    if len(row.values) > 0:
                        self.output_str += "\n" 
            
       
        return self.output_str
        pass
    
    def evaluate_predicate(self, predicate: Predicate) -> Predicate: 
        name_of_query = predicate.name
        new_relation = copy.deepcopy(self.database[name_of_query])
        #IMPLEMENTATION OF SELECT 1 AND SELECT 2
        parameterIndex: int = 0
        IDs : list[str] = []
        colIndexes : list[int] = []
        index1:int = 0
        for parameter in predicate.parameters:
            #parameterIndex += 1
            dict_of_queries: Dict(str, int) = {}
            dict_of_queries = {parameter, parameterIndex}
            isConst : bool = 0
            isID: bool = 0
            haveSeenID: bool = 0
            
            if parameter[0] == '\'':
                isConst = 1
            else:
                isID = 1
            
            if isConst == 1:
                new_relation = new_relation.select1(parameter, parameterIndex)
                #colIndexes.append(parameterIndex)
                #IDs.append(parameter)
                parameterIndex += 1
            #if is a constant SELECT1
            #if we have seen it SELECT2
            elif isID == 1:
                #for index in IDs:
                    #if index in IDs == parameter:
                        #haveSeenID = 1
                        #index1 = dict_of_queries[parameter]
                        
                #if haveSeenID == 1:
                if parameter in IDs:
                    #index1 = dict_of_queries[parameter]
                    index1 = IDs.index(parameter)
                    #colIndexes.append(parameterIndex)
                    #IDs.append(parameter)
                    new_relation = new_relation.select2(index1, parameterIndex)
                    parameterIndex += 1
                else:
                    colIndexes.append(parameterIndex)
                    index1 = parameterIndex
                    parameterIndex += 1
                    IDs.append(parameter)



                #if we have not seen it we are going to mark add to helper variables (our dict and lists)
        #IMPLEMENTATION OF PROJECT
        new_relation = new_relation.project(colIndexes)
        
        #print(new_relation)
        #implementation of RENAME
        new_relation = new_relation.rename(Header(IDs))
        #print(new_relation.rename(IDs))

        return new_relation

        
    def interpret_rules(self) -> None:
        # fixed point algorithm to evaluate rules goes here: #move from interprate query to interpret predicate
        #self.output_str += f"Rule Evaluation\n"
        og_set: set()
        curr_graph: Graph = Graph()
        adjacencyList = curr_graph.makeAdjacencyList(self.datalog_program.rule_list)
        #self.output_str += f"{adjacencyList}"
        self.output_str += adjacencyList
        curr_graph.depthFirstSearch()
        curr_graph.depthFirstSearchSCC()
        SCCs = curr_graph.SCCs
        #for ruleIndex in range(len(self.datalog_program.rule_list)):
            #curr_graph.createPostorder(curr_graph.reverseList[ruleIndex])
            #SCCs: list[set[int]] = curr_graph.findSCCs(curr_graph.reverseList[ruleIndex])
        curr_evaluated_rule: int = 0
        self.output_str += f"\nRule Evaluation\n"
        sccVal:int = 0
        sccString:str = ""
        for currSCC in SCCs:
            if len(currSCC) == 0:
                pass
            self.output_str += f"SCC: " #this puts [] just currSCC puts {} i just want the val
            counter = 0
            for val in currSCC:
                #sccString = f"R{val},"
                self.output_str += f"R{val},"
                #if counter < len(currSCC) - 1:
                    #self.output_str += f","
                #counter += 1
            self.output_str = self.output_str[:-1]
            self.output_str += f"\n"
                
            ruleCounter: int = 0
            changed: bool = True
            while changed == True:
                changed = False
                ruleCounter += 1
                for ruleIndex in currSCC:
                    sccVal = ruleIndex
                    self.output_str += f"{self.datalog_program.rule_list[ruleIndex].to_string()}\n"
                    evaluated_rule = self.evaluate_rule(self.datalog_program.rule_list[ruleIndex])
                    
                    if evaluated_rule > 0:
                        changed = True
                listSCC = list(currSCC)
                if len(currSCC) == 1 and listSCC[0] not in curr_graph.forwardList[listSCC[0]].dependencies:
                    break
        #self.output_str += f"\nSchemes populated after {ruleCounter} passes through the Rules.\n\n" # was evaluated rule
            self.output_str += f"{ruleCounter} passes: "
            for index in currSCC:
                self.output_str += f"R{index},"
            self.output_str = self.output_str[:-1]
            self.output_str += f"\n"
        return self.output_str
        pass
    
    # this function should return the number of unique tuples added to the database
    def evaluate_rule(self, rule: Rules) -> int:
        colsToProject : list[int] = []
        variableNames: list = []
        # Step 1:
        resultList: list = [] #update
        changed: bool = True
        #numRules: int = 0
        #while (changed == True): #move this to interpret
            #changed = False
        for predicate in rule.rule_list:
            result = self.evaluate_predicate(predicate)
            #print(result)
            #colIndexes += 
            resultList.append(result)
            #print(resultList)
        new_result: Relation
        new_result = resultList[0]
        if len(resultList) >= 2:
            for result in resultList:
                new_result = new_result.natural_join(result)
    
        for i in rule.head_predicate.parameters: #trying to use the tuple in the head predicate
            index = 0
            for j in new_result.header.values:
                if j == i:
                    colsToProject.append(index)
                index += 1
                        
        new_result = new_result.project(colsToProject)
        #print(new_result.header.values)

        val_to_rename: Header = Header(rule.head_predicate.parameters)
        new_result = new_result.rename(val_to_rename) #change
        size_before: int = len(self.database[rule.head_predicate.name].rows)
        #print(size_before)

      
        self.database[rule.head_predicate.name], self.output_str = self.database[rule.head_predicate.name].union(new_result, self.output_str, rule) #change
        
        size_after: int = len(self.database[rule.head_predicate.name].rows)
        #print(size_after)
        
        
        return size_after - size_before