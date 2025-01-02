import re;
from mapping.products import kql_product_mapping
from mapping.services import kql_service_mapping
from mapping.fields import kql_field_mapping
from GenerateRule import *

class Query:


#-------------------------Constructor------------------------#

    def __init__(self, query):
        
        self.table = self.extract_table(query)
        self.project = self.extract_project(query)
        self.data_source = self.extract_data_source(query)
        self.fields = self.extract_field(query)


#----------------Constructor's Helper Functions---------------#

    
    def extract_table(self, query):  #TODO: do we need to make sure table == "events_all"?
        match = re.match(r"^(\S+)\s*\r?\n?\|", query)
        if match:
            return match.group(1)
        else : raise ValueError("Illegal input: Expected a table.")
        

    def extract_project(self, query):
        matches = re.findall(r"(?<=\|)\s*project\s+([^\|]+)", query)
        projects = []
        
        for match in matches:
            columns = [column.strip() for column in match.split(',')]
            # if "" in col_to_check:
            #     raise ValueError("Illegal input: Expected a project.")  TODO: (shira) to my opinion these line are not necessary
            projects.extend(columns)                                     #TODO:  (QUESTION) is it ok to have multiple columns with same names?(legal)

        return projects


    def extract_data_source(self, query):
        pattern = r"data_source_type_id\s*==\s*(\d+)|data_source_type_id\s+in\s*\(\s*(\d+(?:\s*,\s*\d+)*)\s*\)"
        matches = re.findall(pattern, query)
        numbers = []

        for match in matches:
            if match[0]:  
                numbers.append(int(match[0]))
            if match[1]:  
                numbers.extend(map(int, match[1].split(',')))

        return numbers

  
    def extract_field(self, query):
        fields = self.clean_unnecessary_data(query)
        fields = self.build_fields_dict(fields)
        return fields


#-----------------------Mapping Functions---------------------#

    #TODO: what description more suitable: map or handle?
    def map_project(self):
        fields = set()

        for pro in self.project:
            column = kql_field_mapping.get(pro, None)
            if column is None:
                raise ValueError(f'ERROR: column : {pro} does not exist in table: {self.table}.')
            fields.add(column)

        return fields


    def map_data_source(self):
        products = set()
        services = set()

        for num in self.data_source:

            collected_products = {kql_product_mapping[num]} if num in kql_product_mapping else set()

            if num in kql_service_mapping:
                value = kql_service_mapping[num]
                collected_services = set(value) if isinstance(value, list) else {value}
            else:
                collected_services = set()

            if not collected_products and not collected_services:
                print(f"ERROR: the number {num} did not match any key in either mapping!")  #TODO: should be an error?
                break

            products = products.union(collected_products)
            services = services.union(collected_services)

        return products, services


    def map_field(self, data):
        if isinstance(data, dict):
            return {key: self.map_field(value) if key == 'operands' else value
                    for key, value in data.items()}
        elif isinstance(data, list):
            return [self.map_field(item) for item in data]
        elif isinstance(data, tuple):
            if data[0] in kql_field_mapping:
                return kql_field_mapping[data[0]], *data[1:]
        return data



# def map_field(self, detection):
#         for t in detection["operands"]:
#             if type(t) is tuple:
#                 detection["operands"].append((kql_field_mapping.get(t[0], t[0]), t[1], t[2]))
#             else:
#                 self.map_field(t)
#         return detection


#--------------------------Functions--------------------------#


    def parse_to_rule(self):

        mapped_project = self.map_project()
        mapped_data_source = self.map_data_source()
        mapped_fields = self.map_field(self.fields.copy())

        rule = GenerateRule(mapped_project, mapped_data_source, mapped_fields)
        
        return rule.finalize_rule()
    

#-----------------------Helper Functions----------------------#


    def clean_unnecessary_data(self, query):
        start_index = query.find("where") + len("where")

        if start_index == -1 : 
            return ""
        else : 
            query_after_where = query[start_index:]

        res = re.sub(r"(?:and|or)?\s*data_source_type_id\s*(?:==\s*\d+|in\s*\(\s*\d+(?:\s*,\s*\d+)*\s*\))\s*(?:and|or)?","", query_after_where)
        res = re.sub(r"\|\s*project\s+([^\|]+)", "" , res)
        
        return res.strip(" ")


    def build_fields_dict(self, fields):
        array_operator = ['in', 'in~' 'has_all']
        logical_op = ['and', 'or', '(', ')']
        stack = []

        current = {"logical operation": None, "operands": []}

        fields.replace("matches regex", "matches_regex")
        tokens = re.findall(r'[^\s()]+|and|or|[()]', fields)
        operators_and_operands = []
        i = 0
        while i < len(tokens):
            if tokens[i] not in logical_op:
                for_tuple = tokens[i: i + 2]
                if for_tuple[1] in array_operator:
                    counter = 1
                    res_string = ""
                    while counter + i < len(tokens) and tokens[counter + i] != ")":
                        counter += 1
                        res_string += tokens[counter + i]
                    i = counter + i + 1
                    for_tuple.append(res_string)
                    operators_and_operands.append(tuple(for_tuple))
                else:
                    for_tuple = tokens[i: i + 3]
                    operators_and_operands.append(tuple(for_tuple))
                    i = i + 3
            else:
                operators_and_operands.append(tokens[i])
                i = i + 1
        for op in operators_and_operands:
            if op == "(":
                # Push current context to stack and start a new one
                stack.append(current)
                current = {"logical operation": None, "operands": []}
            elif op == ")":
                # Finish the current context and attach it to the parent
                last = current
                current = stack.pop()
                current["operands"].append(last)
            elif op in {"and", "or"}:
                # Set the operator
                if current["logical operation"] is None:
                    current["logical operation"] = op
                elif current["logical operation"] != op:
                    raise ValueError("Mixed operators without parentheses are not allowed.")
            else:
                # It's an operand (e.g., a, b, c)
                current["operands"].append(op)

        if stack:
            raise ValueError("Unmatched parentheses in expression.")

        return current
    




#------------------------TESTING (TEMPORARY)----------------------#
query = ("events_all\n| project _Hashes \n | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and _eventName startswith 'UpdateFunctionConfiguration'")
query2 = ("events_all\n| project _Hashes \n | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and  _eventName startswith 'UpdateFunctionConfiguration' and _destination.port in (8080, 21, 80, 23, 50000, 1521, 27017, 1433, 11211, 3306, 15672, 5900, 5901, 5902, 5903, 5904) ")
query3= "events_all\n | where data_source_type_id==11 and _eventSource =~ 'lambda.amazonaws.com' and (_USER startswith '#-' or _USER matches_regex '\\#.*4294967295')"

parse_query = Query(query3)
print(parse_query.map_project())
print(parse_query.map_data_source())
print(parse_query.fields)
print(parse_query.map_field(parse_query.fields.copy()))



# events_all
# | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and _eventName startswith 'UpdateFunctionConfiguration'
#
# logsource:
#     product: aws
#     service: ..
# detection:
#     selection:
#         eventSource: lambda.amazonaws.com
#         eventName|startswith: 'UpdateFunctionConfiguration'
#     condition: selection