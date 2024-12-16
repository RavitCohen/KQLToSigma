import re;
from mapping.products import kql_product_mapping
from mapping.services import kql_service_mapping
from mapping.fields import kql_field_mapping
from GenarateRule import *

class Query:

#-------------------------Constructor------------------------#

    def __init__(self, query):
        
        self.table = self.extract_table(query)
        self.project = self.extract_project(query)
        self.data_source = self.extract_data_source(query)
        self.fields = self.extract_field(query)


#----------------Constructor's Helper Functions---------------#

    def extract_table(self, query):
        regex = r"^(\S+)\s*\r?\n?\|"
        match = re.match(regex, query)

        if not match:
            raise ValueError("Illegal input: Expected a table.")

        return match.group(1)


    # def extract_project(self, query):
    #     regex = r"(?<=\|)\s*project\s+([^\|]+)"
    #     matches = re.findall(regex, query)
    #     if not matches:
    #         raise ValueError("Illegal input: Expected a project.")
    #     project = []
    #     for match in matches:
    #         col_to_check = [col.strip() for col in match.split(',')]
    #         print (col_to_check)
    #         if "" in col_to_check:
    #             raise ValueError("Illegal input: Expected a project.")
    #         project.extend(col_to_check)
    #
    #     return project

    def extract_project(self, query):
        regex = r"(?<=\|)\s*project\s+([^\|]+)"
        matches = re.findall(regex, query)
        project = []
        for match in matches:
            col_to_check = [col.strip() for col in match.split(',')]
            if "" in col_to_check:
                raise ValueError("Illegal input: Expected a project.")
            project.extend(col_to_check)

        return project


    def extract_data_source(self, query):
        pattern = r"data_source_type_id\s*=\s*(\d+)|data_source_type_id\s+in\s*\(\s*(\d+(?:\s*,\s*\d+)*)\s*\)"
        matches = re.findall(pattern, query)
        numbers = []

        for match in matches:
            if match[0]:  # If the first group (for = ) is not empty
                numbers.append(int(match[0]))
            if match[1]:  # If the second group (for in () ) is not empty
                numbers.extend(map(int, match[1].split(',')))
        self.data_source=numbers

        return numbers

    #TODO: change names of function and structure
    #Return all the fields as a string and split in the handle
    def extract_field(self, query):
        fields = self.helper_extract_field(query)
        res = self.build_dict_from_filed(fields)
        return res

    def helper_extract_field(self, query):
        start_index = query.find("where")

        if start_index != -1:
            query_from_where = query[start_index + len("where"):]
        else:
            print("'where' not found")
            return

        res = re.sub(r"(?:and|or)?\s*data_source_type_id\s*(?:=\s*\d+|in\s*\(\s*\d+(?:\s*,\s*\d+)*\s*\))\s*(?:and|or)?",
                     "", query_from_where)
        return res.strip()

    def build_dict_from_filed(self, fields):
        stack = []
        current = {"logical operation": None, "operands": []}

        tokens = re.findall(r'[^\s()]+|and|or|[()]', fields)
        operators_and_operands = []
        i = 0
        while i < len(tokens):
            if tokens[i] != "and" and tokens[i] != "or" and tokens[i] != "(" and tokens[i] != ")":
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

#--------------------------Functions-------------------------#

    # TODO: implement after we'll get a fields mapping
    def handle_project(self):
        fields = set()

        for pro in self.project:
            column = kql_field_mapping.get(pro, None)
            if column is None:
                raise ValueError(f'ERROR: {pro} column does not exist in table: {self.table}.')
            fields.add(column)

        return fields



    def handle_data_source(self):
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
                print(f"ERROR: the number {num} did not match any key in either mapping!")
                break

            products = products.union(collected_products)
            services = services.union(collected_services)

        return products, services


    def parse_to_rule(self):

        mapped_project = self.handle_project()
        mapped_data_source = self.handle_data_source()
        print("mapped_project", mapped_project)
        print("mapped_data_source", mapped_data_source)
        return
        #mapped_fields = self.handle_field()

        #rule = GenarateRule(mapped_project, mapped_data_source, mapped_fields)

        #return rule.finalize_rule()


#TESTING TEMPORARY
query = ("events_all\n| project Hashes \n | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and _eventName startswith 'UpdateFunctionConfiguration'")
parse_query = Query(query)
print(parse_query.table)
print(parse_query.project)
print(parse_query.data_source)
print(parse_query.fields)
parse_query.parse_to_rule()
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