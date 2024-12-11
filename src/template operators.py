import re


def parse_logical_expression(expression: str):

    def parse(expression):
        stack = []
        current = {"operator": None, "operands": []}

        tokens = re.findall(r'[^\s()]+|and|or|[()]', expression)
        print(tokens)
        for token in tokens:
            if token == "(":
                # Push current context to stack and start a new one
                stack.append(current)
                current = {"operator": None, "operands": []}
            elif token == ")":
                # Finish the current context and attach it to the parent
                last = current
                current = stack.pop()
                current["operands"].append(last)
            elif token in {"and", "or"}:
                # Set the operator
                if current["operator"] is None:
                    current["operator"] = token
                elif current["operator"] != token:
                    raise ValueError("Mixed operators without parentheses are not allowed.")
            else:
                # It's an operand (e.g., a, b, c)
                current["operands"].append(token)

        if stack:
            raise ValueError("Unmatched parentheses in expression.")

        return current

    return parse(expression)


# Example usage
expression1 = "_eventSource =~ 'lambda.amazonaws.com' and _eventName startswith 'UpdateFunctionConfiguration'"
expression2 = "('hygv:jhbh' and (b or c)) or a or c"
parsed_structure1 = parse_logical_expression(expression1)
parsed_structure2 = parse_logical_expression(expression2)

print(parsed_structure1)
print(parsed_structure2)
