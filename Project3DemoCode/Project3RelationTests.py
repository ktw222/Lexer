# help slides:
# https://docs.google.com/presentation/d/1I1rmBa7SKR8g6UliwpAZmsorvSprK4ZXzhUgE-nlVB4/edit
from Relation import Relation
from Header import Header
from Row import Row
from Interpreter import Interpreter

# remove this and delete the file 
# after you add in your code from project 2
#from project_2_classes.parser import DatalogProgram
from class_stubs import * 

base_row_1: Row = Row(['\'12345\'','\'Charlie\'','\'12 Apple St.\'','\'555-1234\''])
base_row_2: Row = Row(['\'67890\'','\'Lucy\'','\'34 Pear Ave.\'','\'555-5678\''])
base_row_3: Row = Row(['\'33333\'','\'Snoopy\'','\'12 Apple St.\'','\'555-1234\''])
base_row_4: Row = Row(['\'33333\'','\'Charlie\'','\'12 Apple St.\'','\'Charlie\''])
base_row_5: Row = Row(['\'33333\'','\'Snoopy\'','\'12 Apple St.\'','\'Snoopy\''])
base_header: Header = Header(["S", "N", "A", "P"])
base_relation: Relation = Relation("SNAP", base_header, set([base_row_1, base_row_2, base_row_3, base_row_4, base_row_5]))

def test_select1():
    print('select1("\'Charlie\'", 1):')
    print(base_relation.select1("\'Charlie\'", 1).__str__())
    print('select("\'12 Apple St.\'", 2):')
    print(base_relation.select1("\'12 Apple St.\'", 2).__str__())
    try:
        print('select1("\'Charlie\'",-1):')
        print(base_relation.select1("\'Charlie\'", -1).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")
        
    try:
        print('select1("\'Charlie\'",4):')
        print(base_relation.select1("\'Charlie\'", 4).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")

def test_select2():
    print('select2(1,3):')
    print(base_relation.select2(1, 3).__str__())
    print('select2(0,1):')
    print(base_relation.select2(0,1).__str__())
    try:
        print('select2(-1,1):')
        print(base_relation.select2(-1,0).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")
    try:
        print('select2(0,4):')
        print(base_relation.select2(0,4).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")

def test_rename():
    print('rename(["studentID", "studentName", "studentAddress", "studentPhoneNum"]):')
    print(base_relation.rename(Header(["studentID", "studentName", "studentAddress", "studentPhoneNum"])).__str__())
    try:
        print('rename(["studentID", "studentName"]):')
        print(base_relation.rename(Header(["studentID", "studentName"])).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")

def test_project():
    print('project([1]):')
    print(base_relation.project([1]).__str__())
    
    print('project([2]):')
    print(base_relation.project([2]).__str__())
    
    print('project([3, 1]):')
    print(base_relation.project([3, 1]).__str__())
    
    print('project([3, 2, 1, 0]):')
    print(base_relation.project([3, 2, 1, 0]).__str__())
    try:
        print('project([4, 1])):')
        print(base_relation.project([4, 1]).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")
        
        
    try:
        print('project([-1, 1])):')
        print(base_relation.project([4, 1]).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")
    
    print('project([3, 2, 1, 0]):')
    print(base_relation.project([3, 2, 1, 0]).__str__())
    
    # this should have 1 row, with a length of 0, why is this the case?
    print('project([]):')
    print(base_relation.project([]).__str__())


# __name__ 
if __name__=="__main__": 
    print("Base Relation")
    print(base_relation.__str__())
    test_select1()
    test_select2()
    test_rename()
    test_project()
    
    

# example code for the actual project main

def project3():
    lexer: Lexer = Lexer()
    lexer.run()
    tokens: list[Token] = lexer.getTokens()

    parser: Parser = Parser()
    parser.run(tokens)
    datalog_program: DatalogProgram = parser.get_program()

    interpreter: Interpreter = Interpreter()
    print(interpreter.run(datalog_program))