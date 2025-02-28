import re


# -----------------------Helper Functions----------------------#
def clean_unnecessary_data(query):
    start_index = query.find("where") + len("where")

    if start_index == -1:
        return ""
    else:
        query_after_where = query[start_index:]

    res = re.sub(r"(?:and|or)?\s*data_source_type_id\s*(?:==\s*\d+|in\s*\(\s*\d+(?:\s*,\s*\d+)*\s*\))\s*(?:and|or)?",
                 "", query_after_where)
    res = re.sub(r"\|\s*project\s+([^\|]+)", "", res)

    return res.strip(" ")


def build_fields_dict(fields):
    should_pop = 0
    array_operator = ['in', 'in~', 'has_all']
    logical_op = ['and', 'or','not', '(',')']  #added NOT operator
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
        elif op in {"and", "or", "not"}: #added here "not"
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



 
 
 
 
 
 #-----used in SigmaRuleGenerator.py-----#
 
 
def parse_to_list(s) -> list:
    """  
    Convert a comma-separated string in parentheses into a list.
    """
    return [item.strip(" '") for item in s.strip("() ").split(",")]           
 
 
def simplify_condition(condition) :
    new_condition = standardize_condition(condition)    
    
    match "or" in condition, "and" in condition, "not" in condition:
        case (False, False, False):
            new_condition = "selection1"
        case (True, False, False):
            new_condition = "1 of selection*"
        case (False, True, False):
            new_condition = "all of selection*"
        case _:
            pass
    return new_condition   


def standardize_condition(condition):
    """
    Cleans and formats a logical condition string by:
    - Removing leading/trailing 'or' or 'and'.
    - Eliminating unnecessary parentheses around single elements.
    - Condensing multiple spaces into one.
    """
    # Remove leading/trailing spaces
    condition = condition.strip()

    # Remove unnecessary 'or' or 'and' at the beginning or end
    condition = re.sub(r'^(or|and)\s+', '', condition)
    condition = re.sub(r'\s+(or|and)$', '', condition)

    condition = replace_single_word_parentheses(condition)
    condition = re.sub(r'\s+', ' ', condition)
    return condition


def replace_single_word_parentheses(s):
    # This function replaces (single_word) with single_word, keeping everything else intact.
    
    # Function to process each match
    def process_match(match):
        content = match.group(1).strip()  # Extract content inside parentheses
        
        # If the content is a single word, return just the word
        if len(content.split()) == 1:
            return content
        
        # Otherwise, return the entire match (which keeps the parentheses)
        return match.group(0)
    
    # Regular expression to match content inside parentheses, handling nested parentheses
    pattern = r'\(([^()]*?)\)'

    # Replace all matches in the string
    result = re.sub(pattern, process_match, s)
    
    return result


def flatten_single_item_lists_in_dict(my_dict):
    """  
    Recursively replace single-item lists in a dictionary with their sole element.  
    """  
    for key,value in my_dict.items():
        if type(value) is dict: 
            flatten_single_item_lists_in_dict(value)
        elif type(value) is list and len(value) == 1: 
            my_dict[key] = value[0]
        elif type(value) is list:
            for element in value:
                if type(element) is dict:
                    flatten_single_item_lists_in_dict(element)
        

def remove_empty_keys(my_dict):
    """  
    Recursively remove empty values and dictionaries from a dictionary.  
    """ 
    
    keys_to_delete = []

    for key, value in my_dict.items():
        if type(value) is dict:
            remove_empty_keys(value)
        if not value:  # If value is empty
            keys_to_delete.append(key)
        elif type(value) is list:
            for element in value:
                if type(element) is dict:
                    remove_empty_keys(element)

    for key in keys_to_delete:
        del my_dict[key]  











# Example usage:
input_string = "akfrmgkir mkfgjr dvmkfv (shira ) and (slecr2 and (sle ))"
processed_string = replace_single_word_parentheses(input_string)
print(processed_string)








