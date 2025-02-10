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
    array_operator = ['in', 'in~' 'has_all']
    logical_op = ['and', 'or', '(', ')']
    stack = []
    current = {"logical operation": None, "operands": []}

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
                    res_string += " " + tokens[counter + i]
                i = counter + i + 1
                for_tuple.append(res_string)
                operators_and_operands.append(tuple(for_tuple))
            else:
                for_tuple = tokens[i: i + 2]
                to_check = tokens[i + 2]
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


def pretty_print_dict(data, indent=0):
    spacing = '    '  # Define the indentation size (4 spaces)
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{spacing * indent}{key}:")
            pretty_print_dict(value, indent + 1)
        else:
            print(f"{spacing * indent}{key}: {value}")