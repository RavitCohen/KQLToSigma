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
            #if "" in col_to_check:
             #   raise ValueError("Illegal input: Expected a project.")  #TODO: (shira) to my opinion these line are not necessary
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
        #defenitions:
        logical_op = ['and', 'or','(',')']
        operators_and_operands = []
        i = 0

        # Dealing with an option whose field consists of two words
        self.fix_fileds_two_word(fields)

        tokens = re.findall(r'[^\s()]+|and|or|[()]', fields)
        len_tokens = len(tokens)

        while i < len_tokens:
            if tokens[i] not in logical_op:
                i, param_tuple = self.create_tuple_from_token(i, len_tokens, tokens)
                operators_and_operands.append(tuple(param_tuple))
            else: #tokens[i] in logical_op:
                operators_and_operands.append(tokens[i])
                i = i + 1

        dict_logic = self.create_dict_logic(operators_and_operands)

        return dict_logic


#------------helper function--------------#
    def fix_fileds_two_word(self, fields):
        fields.replace("matches regex" , "matches_regex")

    def create_tuple_from_token(self, i, len_tokens, tokens):
        array_operator = ['in', 'in~', 'has_all']
        param = tokens[i: i + 2]

        if param[1] in array_operator:
            counter = 1
            res_string = ""
            while counter + i < len_tokens and tokens[counter + i] != ")":
                i, param = self.create_string_from_list(counter, res_string, param, len_tokens, tokens, i)

        else: #param[1] not in array_operator
            to_check = tokens[i + 2]
            if to_check.startswith("'") and not to_check.endswith("'") or to_check == "'":
                counter = 3
                res_string = to_check
                while counter + i < len_tokens and not tokens[counter + i].endswith("'"):
                    i, param = self.create_string_from_list(counter, res_string, param, len_tokens, tokens, i)
            else:
                param = tokens[i: i + 3]
                param[2] = param[2].strip("'")
                i = i + 3

            return i, tuple(param)

    def create_string_from_list(self, counter, res_string, param, len_tokens, tokens, i):
        res_string += " " + tokens[counter + i]
        counter += 1
        i = counter + i + 1
        if counter + i < len_tokens:
            res_string += " " + tokens[counter + i]
        param.append(res_string)
        param[2] = param[2].strip("'")
        return i, param

    def create_dict_logic(self, operators_and_operands):
        dict_logic = {"logical operation": None, "operands": []}
        stack = []

        for op in operators_and_operands:
            if op == "(":
                # Push current context to stack and start a new one
                stack.append(dict_logic)
                dict_logic = {"logical operation": None, "operands": []}
            elif op == ")":
                # Finish the current context and attach it to the parent
                last = dict_logic
                dict_logic = stack.pop()
                dict_logic["operands"].append(last)
            elif op in {"and", "or"}:
                # Set the operator
                if dict_logic["logical operation"] is None:
                    dict_logic["logical operation"] = op
                elif dict_logic["logical operation"] != op:
                    raise ValueError("Mixed operators without parentheses are not allowed.")
            else:
                # It's an operand (e.g., a, b, c)
                dict_logic["operands"].append(op)
        if stack:
            raise ValueError("Unmatched parentheses in expression.")

        return dict_logic

#--------------delete after---------------
    def pretty_print_dict(self, data, indent=0):
        spacing = '    '  # Define the indentation size (4 spaces)
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{spacing * indent}{key}:")
                self.pretty_print_dict(value, indent + 1)
            else:
                print(f"{spacing * indent}{key}: {value}")


#------------------------TESTING (TEMPORARY)----------------------#
query = "events_all\n| _CommandLine contains 'base64' and _CommandLine contains '|bash' "
# query = ("events_all\n| project _Hashes | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and  _eventName startswith 'UpdateFunctionConfiguration' and _destination.port in (8080, 21, 80, 23, 50000, 1521, 27017, 1433, 11211, 3306, 15672, 5900, 5901, 5902, 5903, 5904) ")
# query= "events_all\n| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and (_eventSource =~ 'sts.amazonaws.com' and _eventName =~ 'AssumeRoleWithSAML') or (_eventSource =~ 'iam.amazonaws.com' and _eventName =~ 'UpdateSAMLProvider')"
# #
parse_query = Query(query)
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
