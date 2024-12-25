import re


def parse_logical_expression(expression: str):

    def parse(expression):
        stack = []
        current = {"logical operation": None, "operands": []}

        tokens = re.findall(r'[^\s()]+|and|or|[()]', expression)
        print(tokens)
        operators_and_operands = []
        i = 0
        while i < len(tokens):
            if tokens[i] != "and" and tokens[i] != "or" and tokens[i] != "(" and tokens[i] != ")":
                for_tuple = tokens[i: i+3]
                operators_and_operands.append(tuple(for_tuple))
                i = i + 3
            else:
                operators_and_operands.append(tokens[i])
                i = i + 1
        print(operators_and_operands)
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

    return parse(expression)

def parse (expression: str):
    start_index = expression.find("where")

    if start_index != -1:
        result = expression[start_index+len("where"):]
    else:
        print("'where' not found")
        return

    res = re.sub(r"(?:and|or)?\s*data_source_type_id\s*(?:=\s*\d+|in\s*\(\s*\d+(?:\s*,\s*\d+)*\s*\))\s*(?:and|or)?","",result)
    return res.strip()

query = ("events_all\n| project defef \n | where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and _eventSource =~ 'lambda.amazonaws.com' and  _eventName startswith 'UpdateFunctionConfiguration' ")
ex1 = parse(query)
print(ex1)
# parsed_structure1 = parse_logical_expression(ex1)
# print(parsed_structure1)


# Example usage
expression1 = "_destination.port in (8080, 21, 80, 23, 50000, 1521, 27017, 1433, 11211, 3306, 15672, 5900, 5901, 5902, 5903, 5904)"
expression2 = "(a = d and (b = f or c = t)) or a = f or c = d"
parsed_structure1 = parse_logical_expression(expression1)
parsed_structure2 = parse_logical_expression(expression2)

print(parsed_structure1)
print(parsed_structure2)
