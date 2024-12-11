import re


def parse_logical_expression(expression: str):
    """
    Parse a logical expression and store operators (AND, OR) with their corresponding operands.

    Args:
        expression (str): Logical expression, e.g., "(a and (b or c)) or a or c".

    Returns:
        dict: Parsed structure of operators and operands.
    """

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
expression = "('hygv:jhbh' and (b or c)) or a or c"
parsed_structure = parse_logical_expression(expression)

print(parsed_structure)
