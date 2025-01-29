#-----------------------GLOBAL VARIABLES----------------------#

selection_counter = 1
acc_condition = ""
current_selection_added = 0

comparable_operator = {'==': ':', '=~': ':'}
text_operator = {'contains': '|contains', 'startswith': '|startswith', 'endswith': '|endswith','matches_regex': '|re:'}
array_operator = {'in': '', 'in~': '', 'has_all': '|contains|all'}
operators = {**comparable_operator, **text_operator, **array_operator}

#----------------------CLASS GenerateRule---------------------#
class GenerateRule:

#-------------------------Constructor-------------------------#

    def __init__(self, mapped_project, mapped_data_source, mapped_fields):
        self.rule = {"logsource": {"product": [], "service": []},
                     "detection": {"condition": ""},  
                     "field": []}

        self.assign_project(mapped_project)
        self.assign_logsource(mapped_data_source)
        self.assign_fields_test(mapped_fields)

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


    def assign_fields_test(self, mapped_fields):
        global selection_counter
        
        #Step 1: get the current operator and create a new selection name.
        current_operator = mapped_fields["logical operation"]
        selection_key = f'selection_{selection_counter}'
        selection_counter += 1
        
        #Step 2: add selection to rule with suitable empty value structure.
        match current_operator:
            case "or":
               self.rule["detection"][selection_key] = []
            case "and":
                self.rule["detection"][selection_key] = {}
            case _:
                self.rule["detection"][selection_key] = {} 

        #Step 3: scan the operands and add them under the current selection.
        self.scan_operands(mapped_fields["operands"], selection_key, current_operator)
                
    
    def scan_operands(self, list, key, op):
        global acc_condition
        global current_selection_added
        
        for t in list:
            
            #Case 1: t is tuple:
            if type(t) is tuple:
                
                #update acc_condition.
                if not current_selection_added:
                    acc_condition += key
                    current_selection_added += 1
                
                #Case 1a: AND 
                if op == "and":
                    inner_key = f'{t[0]}{operators[t[1]]}'
                    if inner_key not in self.rule["detection"][key]:
                        self.rule["detection"][key][inner_key] = []
                    self.rule["detection"][key][inner_key].append(t[2])
                    
                #Case 1b: OR 
                elif op == "or":
                    inner_key = f'{t[0]}{operators[t[1]]}'
                    added = False
                    for my_dict in self.rule["detection"][key]:
                        if inner_key in my_dict:
                            my_dict[inner_key].append(t[2])
                            added = True
                            break
                    if not added:
                        self.rule["detection"][key].append({inner_key: [t[2]]})
            
            #Case 2: t is dictionary:
            #Case 2a: dictionary of same operator.
            elif t["logical operation"] == op:
                self.scan_operands(t["operands"], key, op)
            
            #Case 2b: dictionary of different operator.
            else:
                current_selection_added = 0
                acc_condition += " "+ op +" ("
                self.assign_fields_test(t)
                acc_condition += ")"
                

    def finalize_rule(self):
        self.fix_rule()
        self.create_condition()
        return self.rule


#-----------------------Helper Functions----------------------#

    def create_condition(self):
        match "or" in acc_condition, "and" in acc_condition:
            case (False, False):
                self.rule["detection"]["condition"] = "selection_1"
            case (True, False):
                self.rule["detection"]["condition"] = "1 of selection_*"
            case (False, True):
                self.rule["detection"]["condition"] = "all of selection_*"
            case _:
                self.rule["detection"]["condition"] = acc_condition   #TODO: get rid of unnecessary parentheses

    
    def fix_rule(self):
        self.clean_empty_keys(self.rule)
        self.handle_list_of_one_item(self.rule)
        self.reset_selection_numbering()
        
        
    def clean_empty_keys(self, my_dict):
        for key in list(my_dict.keys()):
            value = my_dict[key]
            if type(value) is dict: 
                self.clean_empty_keys(value)
            if not value: 
                del my_dict[key]
          
            
    def handle_list_of_one_item(self, my_dict):
        for key in my_dict:
            value = my_dict[key]
            if type(value) is dict: 
                self.handle_list_of_one_item(value)
            elif type(value) is list and len(value) == 1: 
                my_dict[key] = value[0]


    def reset_selection_numbering(self):
        global acc_condition
        counter = 1
        my_dict = self.rule["detection"]
        for old_key in list(my_dict.keys()):
            if not(old_key == "condition"):
                new_key = f'selection_{counter}'
                counter += 1
                my_dict[new_key] = my_dict.pop(old_key) 
                acc_condition.replace(old_key, new_key)  

        

    


#-------------------examples of queries------------------------#
# query1 = events_all\n| where data_source_type_id==11 and _CommandLine contains 'base64' and ((_CommandLine contains '| bash' or _CommandLine contains '| sh' or _CommandLine contains '|bash' or _CommandLine contains '|sh') or (_CommandLine endswith '|sh' or _CommandLine endswith '|bash' or _CommandLine endswith '|sh' or _CommandLine endswith '|bash'))
# query2 = events_all\n| _CommandLine contains 'base64' and _CommandLine contains '|bash' 
# query3 = events_all\n| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and  _eventName startswith 'UpdateFunctionConfiguration' and _destination.port in (8080, 21, 80, 23, 50000, 1521, 27017, 1433, 11211, 3306, 15672, 5900, 5901, 5902, 5903, 5904) 
# query4 = events_all\n| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and (_eventSource =~ 'sts.amazonaws.com' and _eventName =~ 'AssumeRoleWithSAML') or (_eventSource =~ 'iam.amazonaws.com' and _eventName =~ 'UpdateSAMLProvider')
# query5 = events_all| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' or _eventName startswith 'UpdateFunctionConfiguration'

#old function:
#  def assign_fields_test2(self, mapped_fields):
#         global operators
#         global selection_counter

#         current_operator = None  # 1 = or , 0 = and
#         selection_key = "selection"

#         # check logical operator and update operator_flag
#         if mapped_fields["logical operation"] == "or":
#             current_operator = 1
#             selection_key = f'selection_{selection_counter}'
#             self.rule["detection"][selection_key] = []
#         elif mapped_fields["logical operation"] == "and":
#             current_operator = 0
#             selection_key = f'selection_{selection_counter}'
#             self.rule["detection"][selection_key] = {}
#         selection_counter += 1

#         # scan the operands
#         for t in mapped_fields["operands"]:
#             if type(t) is tuple:
#                 # case1: AND case
#                 if current_operator == 0:
#                     inner_key = f'{t[0]}{operators[t[1]]}'
#                     if inner_key not in self.rule["detection"][selection_key]:
#                         self.rule["detection"][selection_key][inner_key] = []
#                     self.rule["detection"][selection_key][inner_key].append(t[2])

#                 # case2: OR case
#                 elif current_operator == 1:
#                     inner_key = f'{t[0]}{operators[t[1]]}'
#                     added = False
#                     for my_dict in self.rule["detection"][selection_key]:
#                         if inner_key in my_dict:
#                             my_dict[inner_key].append(t[2])
#                             added = True
#                             break
#                     if not added:
#                         self.rule["detection"][selection_key].append({inner_key: [t[2]]})

#             else:
#                 self.assign_fields(t)

