from debugpy.common.timestamp import current

selection_counter = 1
acc_condition = ""

comparable_operator = {'==': ':', '=~': ':'}
text_operator = {'contains': '|contains', 'startswith': '|startswith', 'endswith': '|endswith',
                     'matches_regex': '|re:'}
array_operator = {'in': '', 'in~': '', 'has_all': '|contains|all'}

operators = {**comparable_operator, **text_operator, **array_operator}

class GenerateRule:

#-------------------------Constructor------------------------#

    def __init__(self, mapped_project, mapped_data_source, mapped_fields):
        self.rule = {"logsource": {"product": [], "service": []},
                     "detection": {"condition": ""},  # maybe the value of OR selection will be a list
                     "field": []}

        self.assign_project(mapped_project)
        self.assign_logsource(mapped_data_source)
        self.assign_fields(mapped_fields)

        # [{key , [values]}]
        # selection :{shira: [...] , ravit: [....]}
        # selction1 : [{key1: [values]} , {key2: []} ]


#--------------------------Functions-------------------------#


    def assign_project(self, mapped_project):
        self.rule["field"] = mapped_project


    def assign_logsource(self, mapped_data_source):
        products, services = mapped_data_source
        self.rule["logsource"]["product"] = products
        self.rule["logsource"]["service"] = services


    def assign_fields(self, mapped_fields):
        global operators
        global selection_counter

        current_operator = None  # 1 = or , 0 = and
        selection_key = "selection"

        # check logical operator and update operator_flag
        if mapped_fields["logical operation"] == "or":
            current_operator = 1
            selection_key = f'selection_{selection_counter}'
            self.rule["detection"][selection_key] = []
        elif mapped_fields["logical operation"] == "and":
            current_operator = 0
            selection_key = f'selection_{selection_counter}'
            self.rule["detection"][selection_key] = {}
        selection_counter += 1

        # scan the operands
        for t in mapped_fields["operands"]:
            if type(t) is tuple:
                # case2: AND case
                if current_operator == 0:
                    inner_key = f'{t[0]}{operators[t[1]]}'
                    if inner_key not in self.rule["detection"][selection_key]:
                        self.rule["detection"][selection_key][inner_key] = []
                    self.rule["detection"][selection_key][inner_key].append(t[2])

                    # case2: OR case
                elif current_operator == 1:
                    inner_key = f'{t[0]}{operators[t[1]]}'
                    added = False
                    for my_dict in self.rule["detection"][selection_key]:
                        if inner_key in my_dict:
                            my_dict[inner_key].append(t[2])
                            added = True
                            break
                    if not added:
                        self.rule["detection"][selection_key].append({inner_key: [t[2]]})

            else:
                self.assign_fields(t)

        # TODO: clean all selection that empty and move to genetarte rule


    def finalize_rule(self):
        return self.rule


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

