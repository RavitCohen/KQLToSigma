from src.KQL import KQL
from src.config.operators import operators
from src.utils.mapping import map_projects, map_field, map_log_source
import utils.constants as const


class SigmaRuleGenerator:

    def __init__(self):
        self.rule = {
            "logsource": {
                "product": [],
                "service": []
            },
            "detection": {
                "condition": ""
            },  # maybe the value of OR selection will be a list
            "field": []
        }
        self.fields = []
        self.selection_counter = 0

    def from_query(self, query: KQL):
        products, services = map_log_source(query.data_sources)
        self.set_log_source(products, services)

        fields = map_field(query.fields) # TODO: why copy? copy.deepcopy(map_field(query.fields))
        self.set_detection(fields)

        project = map_projects(query.projects)
        self.set_project(project)

        return self.rule

        # [{key , [values]}]
        # selection :{shira: [...] , ravit: [....]}
        # selction1 : [{key1: [values]} , {key2: []} ]


    def set_project(self, project):
        self.rule["field"] = project

    def set_log_source(self, products, services):
        self.rule["logsource"]["product"] = products
        self.rule["logsource"]["service"] = services

    def set_detection(self, fields):
        # selection_counter = 0 # instead of inside self
        current_operator = None  # 1 = or , 0 = and
        selection_key = "selection"

        # check logical operator and update operator_flag
        logical_operation = fields["logical operation"]
        if logical_operation == const.OR:
            current_operator = logical_operation
            selection_key = f'selection_{self.selection_counter}'
            self.rule["detection"][selection_key] = []
        elif logical_operation == const.AND:
            current_operator = logical_operation
            selection_key = f'selection_{self.selection_counter}'
            self.rule["detection"][selection_key] = {}
        self.selection_counter += 1

        # scan the operands
        for operand in fields["operands"]:
            if type(operand) is tuple:
                # case2: AND case
                if current_operator == const.AND:
                    inner_key = f'{operand[0]}{operators[operand[1]]}'
                    if inner_key not in self.rule["detection"][selection_key]:
                        self.rule["detection"][selection_key][inner_key] = []
                    self.rule["detection"][selection_key][inner_key].append(operand[2])

                    # case2: OR case
                elif current_operator == const.OR:
                    inner_key = f'{operand[0]}{operators[operand[1]]}'
                    added = False
                    for my_dict in self.rule["detection"][selection_key]:
                        if inner_key in my_dict:
                            my_dict[inner_key].append(operand[2])
                            added = True
                            break
                    if not added:
                        self.rule["detection"][selection_key].append({inner_key: [t[2]]})

            else:
                self.set_detection(operand)

        # TODO: clean all selection that empty and move to genetarte rule

    # def pretty_print_dict(self, data, indent=0):
    #     spacing = '    '  # Define the indentation size (4 spaces)
    #     for key, value in data.items():
    #         if isinstance(value, dict):
    #             print(f"{spacing * indent}{key}:")
    #             self.pretty_print_dict(value, indent + 1)
    #         else:
    #             print(f"{spacing * indent}{key}: {value}")

# query = ("events_all\n| where data_source_type_id==11 and _CommandLine contains 'base64' and ((_CommandLine contains '| bash' or _CommandLine contains '| sh' or _CommandLine contains '|bash or _CommandLine contains '|sh') or (_CommandLine endswith '|sh' or _CommandLine endswith '|bash' or _CommandLine endswith '|sh' or _CommandLine endswith '|bash'))")
# print(query.mapped_fields())
# rule = GenerateRule(None,('aws', 'cloudtrail'),{'logical operation': 'and', 'operands': [('_CommandLine', 'contains', "'base64'"), {'logical operation': 'or', 'operands': [{'logical operation': 'or', 'operands': [('_CommandLine', 'contains', "'|bash'"), ('_CommandLine', 'contains', "'|sh'"), ('_CommandLine', 'contains', "'|bash"), ('_CommandLine', 'contains', "'|sh'")]}, {'logical operation': 'or', 'operands': [('_CommandLine', 'endswith', "'|sh'"), ('_CommandLine', 'endswith', "'|bash'"), ('_CommandLine', 'endswith', "'|sh'"), ('_CommandLine', 'endswith', "'|bash'")]}]}]})
# rule.finalize_rule()
# print(rule.mapped_project)
# print(rule.mapped_data_source)
# print(rule.mapped_fields)
# print(rule.rule)
# print(rule.pretty_print_dict(rule.rule))

