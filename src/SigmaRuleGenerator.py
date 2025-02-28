from KQL import KQL
from config.operators import operators, array_operator
from utils.mapping import map_projects, map_field, map_log_source
import utils.constants as const
import utils.helper as helper


class SigmaRuleGenerator:

    def __init__(self):
        self.rule = {
            "logsource": {
                "product": [],
                "service": []
            },
            "detection": {
                "condition": ""
            },  
            "field": []
        }
        self.selection_counter = 0
        self.acc_condition = ""
        self.current_selection_added = 0


    def from_query(self, query: KQL):
        products, services = map_log_source(query.data_sources)
        self.set_log_source(products, services)
        
        fields = map_projects(query.projects)
        self.set_field(fields)
        
        fields_dict = map_field(query.fields) 
        self.set_detection(fields_dict, None)
        self.finalize_rule()

        return self.rule


    def set_log_source(self, products, services):
        self.rule["logsource"]["product"] = products
        self.rule["logsource"]["service"] = services
    
    
    def set_field(self, project):
        self.rule["field"] = project


    def set_detection(self, field_dict, key=None):
        """
        Constructs a detection rule based on logical operations (AND, OR, NOT).
        """
        operator, operands = field_dict["logical operation"], field_dict["operands"]
        selection_key = self.initialize_selection_key(key)
        if key is None:
            self.initialize_detection_structure(selection_key, operator) 
                    
        for operand in operands:
            if type(operand) is tuple:
                self.process_tuple_operand(operand, operator, selection_key)

            elif type(operand) is dict:
                logical_op = operand.get("logical operation")

                if logical_op == operator:
                    self.set_detection(operand, selection_key)
                
                elif operator == None:
                    self.current_selection_added = 0
                    self.set_detection(operand, key=None)
                    
                elif operator == const.NOT :
                    self.current_selection_added = 0
                    self.acc_condition += f'{operator} ('
                    self.set_detection(operand, key=None)
                    self.acc_condition += ")"
                
                elif not self.current_selection_added:
                    self.set_detection(operand, key=None)
                else:
                    self.current_selection_added = 0
                    self.acc_condition += f' {operator} ('
                    self.set_detection(operand, key=None)
                    self.acc_condition += ")"

            else:
                raise TypeError(f"Unexpected operand type: {type(operand)} in set_detection_test")
        
        
    def initialize_selection_key(self, key):
        """ 
        Returns a selection key. If key is None, generates a new one and increments counter.
        """
        if key is None:
            selection_key = f'selection_{self.selection_counter}'
            self.selection_counter += 1
        else:
            selection_key = key
        return selection_key


    def initialize_detection_structure(self, selection_key, operator):
        """
        Initializes the detection structure in the rule dictionary based on the logical operator.
        """
        match operator:
            case const.OR:
                self.rule["detection"][selection_key] = []
            case const.AND:
                self.rule["detection"][selection_key] = {}
            case const.NOT:
                pass  # NOT is handled separately in processing
            case _:
                self.rule["detection"][selection_key] = {}


    def process_tuple_operand(self, operand, operator, selection_key):
        """
        Processes a tuple operand representing a field condition and updates the detection rule.
        """
        field_name, operation, value = operand

        if not self.current_selection_added: 
            self.acc_condition += f'{selection_key} '
            self.current_selection_added += 1
            
        if operation in array_operator:
            value = helper.parse_to_list(value)
        
        inner_key = f"{field_name}{operators[operation]}"

        # Handle AND and OR cases
        if operator in {const.AND, None}:
            if inner_key not in self.rule["detection"][selection_key]:
                self.rule["detection"][selection_key][inner_key] = []
            self.rule["detection"][selection_key][inner_key].append(value)

        elif operator == const.OR:
            added = False
            for entry in self.rule["detection"][selection_key]:
                if inner_key in entry:
                    entry[inner_key].append(value)
                    added = True
                    break

            if not added:
                self.rule["detection"][selection_key].append({inner_key: [value]})

                
    def finalize_rule(self):
        #handle selection_*
        helper.remove_empty_keys(self.rule)
        helper.flatten_single_item_lists_in_dict(self.rule)
        self.reset_selection_numbering()
        
        #handle condition
        condition = helper.simplify_condition(self.acc_condition)
        self.rule["detection"]["condition"] = condition


    def reset_selection_numbering(self) -> None:
        """  
        Renumber selection keys in the detection dictionary,  
        replacing them with sequential names (selection_1, selection_2, etc.).   
        """
        counter = 1
        my_dict = self.rule["detection"]
        for old_key in list(my_dict.keys()):
            if old_key != "condition":
                new_key = f'selection{counter}'
                counter += 1
                my_dict[new_key] = my_dict.pop(old_key) 
                self.acc_condition = self.acc_condition.replace(old_key, new_key)  
        






        

    













# def set_detection_test(self, mapped_fields):
        
#         #Step 1: get the current operator and create a new selection name.
#         current_operator = mapped_fields["logical operation"]
#         selection_key = f'selection_{self.selection_counter}'
#         self.selection_counter += 1
        
#         #Step 2: add selection to rule with suitable empty value structure.
#         match current_operator:
#             case const.OR:
#                 self.rule["detection"][selection_key] = []
#             case const.AND:
#                 self.rule["detection"][selection_key] = {}
#             case const.NOT:
#                 pass    
#             case _:
#                 self.rule["detection"][selection_key] = {} 
            

#         #Step 3: scan the operands and add them under the current selection.
        
#         self.scan_operands(mapped_fields["operands"], selection_key, current_operator)
                

#     def scan_operands(self, list, key, op):
        
#         for t in list:
            
#             #Case 1: t is tuple:
#             if type(t) is tuple:
#                 value = t[2]
#                 if t[1] in array_operator:
#                     value = self.parse_to_list(t[2])
#                 #update acc_condition.
#                 if not self.current_selection_added:
#                     self.acc_condition += key
#                     self.current_selection_added += 1
                
#                 #Case 1a: AND 
#                 if op == const.AND or op == None: 
#                     inner_key = f'{t[0]}{operators[t[1]]}'
#                     if inner_key not in self.rule["detection"][key]:
#                         self.rule["detection"][key][inner_key] = []
#                     self.rule["detection"][key][inner_key].append(value) #changed
                    
#                 #Case 1b: OR 
#                 elif op == const.OR:
#                     inner_key = f'{t[0]}{operators[t[1]]}'
#                     added = False
#                     for my_dict in self.rule["detection"][key]:
#                         if inner_key in my_dict:
#                             my_dict[inner_key].append(value)#changed
#                             added = True
#                             break
#                     if not added:
#                         self.rule["detection"][key].append({inner_key: [value]}) #changed
            
#             #Case 2: t is dictionary:
#             #new added case- need to check
#             elif op == const.NOT:
#                 self.acc_condition += f" {op} ("
#                 self.set_detection_test(t) #not will have only one element which is a dict
#                 self.acc_condition += ")"
                
#             #Case 2a: dictionary of same operator.
#             elif t["logical operation"] == op:
#                 self.scan_operands(t["operands"], key, op)
            
#             #Case 2b: dictionary of different operator.
#             elif not op: #op is none
#                 self.current_selection_added = 0
#                 self.acc_condition += f" {op} ("
#                 self.set_detection_test(t)
#                 self.acc_condition += ")"
            
#             else:
#                 self.set_detection_test(t) #none operator will always have 1 tuple
# def set_detection_test(self, mapped_fields):
        
#         #Step 1: get the current operator and create a new selection name.
#         current_operator = mapped_fields["logical operation"]
#         selection_key = f'selection_{self.selection_counter}'
#         self.selection_counter += 1
        
#         #Step 2: add selection to rule with suitable empty value structure.
#         match current_operator:
#             case const.OR:
#                 self.rule["detection"][selection_key] = []
#             case const.AND:
#                 self.rule["detection"][selection_key] = {}
#             case const.NOT:
#                 pass    
#             case _:
#                 self.rule["detection"][selection_key] = {} 
            

#         #Step 3: scan the operands and add them under the current selection.
        
#         self.scan_operands(mapped_fields["operands"], selection_key, current_operator)
                

#     def scan_operands(self, list, key, op):
        
#         for t in list:
            
#             #Case 1: t is tuple:
#             if type(t) is tuple:
#                 value = t[2]
#                 if t[1] in array_operator:
#                     value = self.parse_to_list(t[2])
#                 #update acc_condition.
#                 if not self.current_selection_added:
#                     self.acc_condition += key
#                     self.current_selection_added += 1
                
#                 #Case 1a: AND 
#                 if op == const.AND or op == None: 
#                     inner_key = f'{t[0]}{operators[t[1]]}'
#                     if inner_key not in self.rule["detection"][key]:
#                         self.rule["detection"][key][inner_key] = []
#                     self.rule["detection"][key][inner_key].append(value) #changed
                    
#                 #Case 1b: OR 
#                 elif op == const.OR:
#                     inner_key = f'{t[0]}{operators[t[1]]}'
#                     added = False
#                     for my_dict in self.rule["detection"][key]:
#                         if inner_key in my_dict:
#                             my_dict[inner_key].append(value)#changed
#                             added = True
#                             break
#                     if not added:
#                         self.rule["detection"][key].append({inner_key: [value]}) #changed
            
#             #Case 2: t is dictionary:
#             #new added case- need to check
#             elif op == const.NOT:
#                 self.acc_condition += f" {op} ("
#                 self.set_detection_test(t) #not will have only one element which is a dict
#                 self.acc_condition += ")"
                
#             #Case 2a: dictionary of same operator.
#             elif t["logical operation"] == op:
#                 self.scan_operands(t["operands"], key, op)
            
#             #Case 2b: dictionary of different operator.
#             elif not op: #op is none
#                 self.current_selection_added = 0
#                 self.acc_condition += f" {op} ("
#                 self.set_detection_test(t)
#                 self.acc_condition += ")"
            
#             else:
#                 self.set_detection_test(t) #none operator will always have 1 tuple

 
