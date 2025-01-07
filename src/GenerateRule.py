from debugpy.common.timestamp import current

selection_counter_and = 0
selection_counter_or = 0


class GenerateRule:

    comparable_operator = {'==':':' , '=~':':'}
    text_operator = {'contains': '|contains:', 'startswith' : '|startswith:', 'endswith':'|endswith:' , 'matches_regex':'|re:'}
    array_operator = {'in':':' , 'in~':':' , 'has_all':'|contains|all:'}
    
    operators = {**comparable_operator,**comparable_operator, **array_operator}


#-------------------------Constructor------------------------#

    def __init__(self, mapped_project, mapped_data_source, mapped_fields):
        self.mapped_project = mapped_project
        self.mapped_data_source = mapped_data_source
        self.mapped_fields = mapped_fields

        self.rule = {   "logsource": {"product": [], "service": []},
                        "detection": {"condition": []},
                        "field": []}



#--------------------------Functions-------------------------#


    def assign_project(self):
        self.rule["field"] = self.mapped_project
        

    def assign_logsource(self):
        products, services = self.mapped_data_source
        self.rule["logsource"]["product"] = products
        self.rule["logsource"]["service"] = services
        
    def assign_fields(self):
        selection_counter_and=0
        current_operator = None

        my_dict = self.mapped_fields
        if my_dict['logical operation'] == 'and':
            for field in my_dict['operands']:
                if isinstance(field, tuple):
                    #TODO: the value not append
                    self.rule['detection'][f'selection_0{selection_counter_and}'] = field
                elif isinstance(field, dict):
                    selection_counter_and += 1
                    self.rule['detection'][f'selection_0{selection_counter_and}'] = field

            #
        # if my_dict['logical operation'] == 'or':
        #     global selection_counter_or
        #     self.rule[(f' selection_1{selection_counter_or}'] =
        #     selection_counter_or+=1

            return

    def finalize_rule(self):
        #TODO: convert self.final_dict to string according by sigma rule
        self.assign_project()
        self.assign_logsource()
        self.assign_fields()
        return  # final string to print

    def pretty_print_dict(self, data, indent=0):
        spacing = '    '  # Define the indentation size (4 spaces)
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{spacing * indent}{key}:")
                self.pretty_print_dict(value, indent + 1)
            else:
                print(f"{spacing * indent}{key}: {value}")

query = ("events_all\n| where data_source_type_id==11 and _CommandLine contains 'base64' and ((_CommandLine contains '|bash' or _CommandLine contains '|sh' or _CommandLine contains '|bash or _CommandLine contains '|sh') or (_CommandLine endswith '|sh' or _CommandLine endswith '|bash' or _CommandLine endswith '|sh' or _CommandLine endswith '|bash'))")
rule = GenerateRule(None,('aws', 'cloudtrail'),{'logical operation': 'and', 'operands': [('_CommandLine', 'contains', "'base64'"), {'logical operation': 'or', 'operands': [{'logical operation': 'or', 'operands': [('_CommandLine', 'contains', "'|bash'"), ('_CommandLine', 'contains', "'|sh'"), ('_CommandLine', 'contains', "'|bash"), ('_CommandLine', 'contains', "'|sh'")]}, {'logical operation': 'or', 'operands': [('_CommandLine', 'endswith', "'|sh'"), ('_CommandLine', 'endswith', "'|bash'"), ('_CommandLine', 'endswith', "'|sh'"), ('_CommandLine', 'endswith', "'|bash'")]}]}]})
rule.finalize_rule()
print(rule.mapped_project)
print(rule.mapped_data_source)
print(rule.mapped_fields)
print(rule.pretty_print_dict(rule.rule))
