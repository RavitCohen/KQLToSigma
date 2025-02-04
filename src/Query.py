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
        print(matches)
        
        for match in matches:
            columns = [column.strip() for column in match.split(',')]
            #if "" in col_to_check:
             #   raise ValueError("Illegal input: Expected a project.")  #TODO: (shira) to my opinion these line are not necessary
            projects.extend(columns)                                     #TODO:  (QUESTION) is it ok to have multiple columns with same names?(legal)

        print(projects)
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

        return list(fields)


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

        return list(products), list(services)


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



#--------------------------Functions--------------------------#

    def parse_to_rule(self):

        mapped_project = self.map_project()
        mapped_data_source = self.map_data_source()
        mapped_fields = self.map_field(self.fields.copy())

        my_rule = GenerateRule(mapped_project, mapped_data_source, mapped_fields).finalize_rule()
        
        return my_rule


#-----------------------Helper Functions----------------------#

    def clean_unnecessary_data(self, query):
        
        start_index = query.find("where")

        if start_index == -1 : 
            start_index = query.find("|") + 1
        else:
            start_index = start_index + len("where")

        query_after_where = query[start_index:]

        res = re.sub(r"(?:and|or)?\s*data_source_type_id\s*(?:==\s*\d+|in\s*\(\s*\d+(?:\s*,\s*\d+)*\s*\))\s*(?:and|or)?","", query_after_where)
        res = re.sub(r"\|\s*project\s+([^\|]+)", "" , res)
        
        return res

    
    def build_fields_dict(self, fields):
        should_pop = 0
        array_operator = ['in', 'in~', 'has_all']
        logical_op = ['and', 'or','(',')']
        stack = []
        current = {"logical operation": None, "operands": []}

        fields = fields.replace("matches regex" , "matches_regex")
        tokens = re.findall(r'[^\s()]+|and|or|[()]', fields)
        operators_and_operands = []
        i = 0
        while i < len(tokens):
            if tokens[i] not in logical_op:
                for_tuple = tokens[i: i+2]
                if for_tuple[1] in array_operator:
                    should_pop = 1
                    if operators_and_operands: 
                        operators_and_operands.pop() #added
                    counter = 1
                    res_string = ""
                    while counter + i < len(tokens) and tokens[counter + i] != ")":
                        counter += 1
                        res_string += " " + tokens[counter+i]
                    i = counter + i + 1
                    for_tuple.append(res_string)
                    for_tuple[2] = for_tuple[2].strip("'")
                    operators_and_operands.append(tuple(for_tuple))
                else:
                    for_tuple = tokens[i: i + 2]
                    to_check = tokens[i+2]
                    if to_check.startswith("'") and not to_check.endswith("'") or to_check == "'":
                        counter = 3
                        res_string = to_check
                        while counter + i < len(tokens) and not tokens[counter + i].endswith("'"):
                            res_string += " " + tokens[counter + i]
                            counter += 1
                        if counter + i < len(tokens):
                            res_string += " " + tokens[counter + i]
                        i = counter + i + 1
                        for_tuple.append(res_string)
                        for_tuple[2] = for_tuple[2].strip("'")
                        operators_and_operands.append(tuple(for_tuple))
                    else:
                        for_tuple = tokens[i: i + 3]
                        for_tuple[2] = for_tuple[2].strip("'")
                        operators_and_operands.append(tuple(for_tuple))
                        i = i + 3
            else:
                if not should_pop:
                    operators_and_operands.append(tokens[i])
                i = i + 1
                should_pop = 0
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
        print(current)
        return current

def pretty_print_dict(self, data, indent=0):
    spacing = '    '  # Define the indentation size (4 spaces)
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{spacing * indent}{key}:")
            self.pretty_print_dict(value, indent + 1)
        else:
            print(f"{spacing * indent}{key}: {value}")




#------------------------TESTING (TEMPORARY)----------------------#

#q = "events_all| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'cloudtrail.amazonaws.com' and (_eventName in~ ('StopLogging', 'UpdateTrail', 'DeleteTrail'))"
#query = Query(q)





#query = "events_all\n| _CommandLine contains 'base64' and _CommandLine contains '|bash' "
# query = ("events_all\n| project _Hashes | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and  _eventName startswith 'UpdateFunctionConfiguration' and _destination.port in (8080, 21, 80, 23, 50000, 1521, 27017, 1433, 11211, 3306, 15672, 5900, 5901, 5902, 5903, 5904) ")
# query= "events_all\n| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and (_eventSource =~ 'sts.amazonaws.com' and _eventName =~ 'AssumeRoleWithSAML') or (_eventSource =~ 'iam.amazonaws.com' and _eventName =~ 'UpdateSAMLProvider')"
# #
#parse_query = Query(query)
#print(parse_query.map_field(parse_query.fields.copy()))



# events_all
# | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' or _eventName startswith 'UpdateFunctionConfiguration'





#------------------------EXAMPLE----------------------#

# query= "events_all\n| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and (_eventSource =~ 'sts.amazonaws.com' and _eventName =~ 'AssumeRoleWithSAML') or (_eventSource =~ 'iam.amazonaws.com' and _eventName =~ 'UpdateSAMLProvider')"
# parse_query = Query(query)
# print(f' data source: {parse_query.map_data_source()}')
# print(f' fields: {parse_query.map_field(parse_query.fields.copy())}')
#
# '''fields: {'logical operation': 'or', 'operands': [{'logical operation': 'and',
#                                                   'operands': [('eventSource', '=~', "'sts.amazonaws.com'"),
#                                                                ('eventName', '=~', "'AssumeRoleWithSAML'")]},
#                                                  {'logical operation': 'and',
#                                                   'operands': [('eventSource', '=~', "'iam.amazonaws.com'"),
#                                                                ('eventName', '=~', "'UpdateSAMLProvider'")]}]}'''
