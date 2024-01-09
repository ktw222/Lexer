class Node:
    #create node class
    #rule num
    #visited bool
    # set int dependency
    def __init__(self, ruleNum):
        self.ruleNum: int = ruleNum
        self.visited: bool = False
        self.dependencies: set[int] = set()

    def Dependency(self, dependency):
        self.dependencies.append(dependency)
    def isVisited(self) -> bool:
        return self.visited
    def Visit(self):
        self.visited = True
    def getDependencyList(self) -> set:
        return self.dependencies
    def getRuleNum(self) -> int:
        return self.ruleNum