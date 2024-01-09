from .Header import Header
from .Row import Row
from Project3DemoCode.project_2_classes.parser import Rules

class Relation:
    def __init__(self, name: str, header: Header, rows: set = None) -> None:
        self.name: str = name
        self.header: Header = header
        if rows is None:
            self.rows = set()
        else:
            self.rows = rows

    
    def __str__(self) -> str:
        output_str: str = ""
        row: Row
        for row in sorted(self.rows):
            output_str += "  "
            sep: str = ""
            for i in range(len(self.header.values)):
                output_str += sep
                output_str += self.header.values[i]
                output_str += "="
                output_str += row.values[i]
                sep = ", "
            output_str += "\n"

        return output_str
    def rules_to_string(self, curr_row) -> str:
        output_str: str = ""
        #row: Row
        #for row in sorted(self.rows):
        output_str += "  "
        sep: str = ""
        for i in range (len(self.header.values)):
            output_str += sep
            output_str += self.header.values[i] #tried replacing i with curr_row
            output_str += "="
            output_str += curr_row.values[i]
            sep = ", "
        output_str += "\n"

        return output_str
        
    def add_row(self, row: Row) -> None:
        if len(row.values) != len(self.header.values):
            raise ValueError("Row and Header were different lengths!")
        self.rows.add(row)
    
    def select1(self, value: str, colIndex: int) -> 'Relation':
        if colIndex < 0 or colIndex >= len(self.header.values):
            raise ValueError("select1: given colIndex was out of bounds")
        new_name: str = self.name + f".select1({value}, {colIndex})"
        new_header: Header = self.header
        new_rows: set = set()

        row: Row
        for row in self.rows:
            if row.values[colIndex] == value:
                new_rows.add(row)
        new_relation = Relation(new_name, new_header, new_rows)
        #print(new_relation)
        return new_relation
    
    def select2(self, index1: int, index2: int) -> 'Relation':
        if index1 < 0 or index1 >= len(self.header.values) or index2 < 0 or index2 >= len(self.header.values):
            raise ValueError("select2: given colIndex was out of bounds")
        new_name: str = self.name + f".select2({index1}, {index2})"
        new_header: Header = self.header
        new_rows: set = set()

        row: Row
        for row in self.rows:
            if row.values[index1] == row.values[index2]:
                new_rows.add(row)
        new_relation = Relation(new_name, new_header, new_rows)
        #print(new_relation)
        return new_relation
    
    
    def rename(self, new_header: Header) -> 'Relation':
        #new_name: str = self.name + f".rename({new_header})"
        return Relation(self.name, new_header, self.rows)

    def project(self, col_indexes: list[int]) -> 'Relation': #loop for header
        new_name: str = self.name
        #loop through my current header
        #only loop through col to project
        cols_to_project = []
        valid_index_range = range(len(self.header.values))
        for index in col_indexes:
            if index in valid_index_range:
                #strim = self.header.values[index]
                cols_to_project.append(self.header.values[index])
            else:
                raise ValueError("project: given colIndex was out of bounds")

        new_header: Header = Header(cols_to_project)
  
        new_relation = Relation(new_name, new_header)
        new_row: set = set()
        row: Row
        projected_rows= []
        for row in self.rows:
            #for index in col_indexes:
                #projected_rows.append(self.rows.values[index]) #this would work for a list of rows but not for a set
                #new_rows.add(row)
                #new_relation.add_row(new_rows)

            projected_rows = [row.values[index] for index in col_indexes]
            new_row = Row(projected_rows)
            new_relation.add_row(new_row)
        #print(new_relation)
        return new_relation
    
    def can_join_rows(self, row1: Row, row2: Row, overlap: list[tuple[int,int]]) -> bool: 
        for x, y in overlap:
            if row1.values[x] != row2.values[y]:
                return False
        return True
    
    def join_rows(self, row1: Row, row2: Row, unique_cols_1: list[int]) -> Row:
        new_row_values: list[str] = []
        for x in unique_cols_1:
            new_row_values.append(row1.values[x])
        new_row_values.extend(row2.values)
        return Row(new_row_values)        
    
    def join_headers(self, header1: Header, header2: Header, unique_cols_1: list[int]) -> Header:
        new_header_values: list[str] = []
        for x in unique_cols_1:
            new_header_values.append(header1.values[x])
        new_header_values.extend(header2.values)
        return Header(new_header_values)     
    
    def natural_join(self, other: 'Relation') -> 'Relation':
        r1: Relation = self
        r2: Relation = other
        
        overlap: list[tuple(int,int)] = []
        unique_cols_1: list[int] = []
        
        for x in range(len(r1.header.values)):
            is_unique = True
            for y in range(len(r2.header.values)):
                if r1.header.values[x] == r2.header.values[y]:
                    overlap.append(tuple([x,y]))
                    is_unique = False
            if is_unique:
                unique_cols_1.append(x)
                    
        h: Header = self.join_headers(r1.header, r2.header, unique_cols_1)

        result: Relation = Relation(r1.name + "|x|" + r2.name, h, set())
        for t1 in r1.rows:
            for t2 in r2.rows:
                if self.can_join_rows(t1,t2,overlap):
                    result_row = self.join_rows(t1, t2, unique_cols_1)
                    result.add_row(result_row)

        
        return result
    def union(self, other: 'Relation', output_str, rule) -> ('Relation', str):
        r1: Relation = self
        r2: Relation = other

        for curr_row in sorted(r2.rows):
            before_rows = len(r1.rows)
            r1.add_row(curr_row)
            after_rows = len(r1.rows)
            if (before_rows < after_rows):
                #curr row gives the right vals
                #ruleRelation = Relation(rule.head_predicate.name, rule.head_predicate.parameters, curr_row.values)
                new_str: str = f"{self.rules_to_string(curr_row)}"
                output_str += f"{new_str}"
            #output_str += f"{before_rows.difference(after_rows)}"
        
        return r1, output_str