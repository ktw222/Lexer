from Project3DemoCode.project_2_classes.parser import Rules
from Project3DemoCode.Node import Node
import pdb
class Graph:
    def __init__(self):
        self.SCCs: list[set(int)] = []
        self.SCCset: set[int] = set() #list potentially
        self.forwardList: map(int, Node) = {}
        self.reverseList: map(int, Node) = {}
        self.postOrder: list[int] = []
        self.reversePostOrder: list[int] = []
        self.output_str = ""
        

    def to_string(self) -> str:
        counter: int = 0
        self.output_str += f"Dependency Graph\n"
        for index in range(len(self.forwardList)):
            self.output_str += f"R{index}:"

            for dependency in sorted(self.forwardList[index].dependencies):
                self.output_str += f"R{dependency},"
                #if dependency < (len(self.forwardList[index].dependencies) - 1):
                    #self.output_str += f","
            if self.forwardList[index].dependencies:
                self.output_str = self.output_str[:-1]
            
            self.output_str += f"\n"
        return self.output_str

       
    def postOrderToString(self):
        #print(self.postOrder)
        pass

    
    def depthFirstSearch(self):

        for ruleIndex in self.reverseList.keys():
            self.reverseList[ruleIndex].visited = False
        for ruleIndex in self.reverseList.keys():
            if not self.reverseList[ruleIndex].visited:
                self.createPostorder(self.reverseList[ruleIndex])
        return
    def createPostorder(self, node: Node) -> list[int]:
        node.Visit()
        
        for dependency in node.dependencies:
            if self.reverseList[dependency].visited != True:
                self.createPostorder(self.reverseList[dependency])
        self.postOrder.append(node.ruleNum)
        #self.postOrder= self.postOrder[::-1]
        #print(self.postOrder)

        #self.postOrderToString()
        return self.postOrder

    def depthFirstSearchSCC(self):
        self.reversePostOrder = self.postOrder[::-1]
        for ruleIndex in self.forwardList.keys():
            self.forwardList[ruleIndex].visited = False
        SccList = []
        for postOrderIndex in self.reversePostOrder:
            if not self.forwardList[postOrderIndex].visited:
                self.findSCCs(self.forwardList[postOrderIndex])
                self.SCCs.append(self.SCCset.copy())
                self.SCCset.clear()
                #self.SCCs= self.SCCs[::-1]
        return
     
        
    def findSCCs(self, node:Node) -> list[set[int]]:
        #self.reversePostOrder = self.postOrder[::-1]
        node.Visit()
       
        for dependency in node.dependencies:
            if self.forwardList[dependency].visited != True:
                self.findSCCs(self.forwardList[dependency])
        

        self.SCCset.add(node.getRuleNum())
        #if self.SCCset:
            #self.SCCs.append(self.SCCset.copy())
            #self.SCCs= self.SCCs[::-1]
        #self.SCCset.clear()
       
        return self.SCCs



    def makeAdjacencyList(self, rules)->str:
        self.forwardList = {i: Node(i) for i in range(len(rules))}
        self.reverseList = {i: Node(i) for i in range(len(rules))}
        
        for ruleIndex in range(len(rules)):
            #node = Node(ruleIndex)
            #self.forwardList[ruleIndex]
            #reverseNode = Node(ruleIndex)
            #self.reverseList[ruleIndex]
            for predicateIndex in range(len(rules[ruleIndex].rule_list)):
                for k in range(len(rules)):
                    if rules[ruleIndex].rule_list[predicateIndex].name == rules[k].head_predicate.name:
                        self.forwardList[ruleIndex].dependencies.add(k)
                        self.reverseList[k].dependencies.add(ruleIndex) 
                      
        
        self.output_str += f"{self.to_string()}"
        return self.output_str

        
        
    