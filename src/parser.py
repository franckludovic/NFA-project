# diane
def add_concatenation(regex):
    """
    Example: a.b|c -> ab.c|
    """
    result = ""
    for i in range(len(regex)):
        c1 = regex[i]

        if i + 1 < len(regex):
            c2 = regex[i + 1]

            result += c1

            # Conditions where concatenation is needed
            if (
                (c1.isalnum() or c1 in ")*+?") and
                (c2.isalnum() or c2 == '(')
            ):
                result += '.'
        else:
            result += c1

    return result


def regex_shunting_yard(regex):
    # Precedence rules for regex
    precedence = {
        '*': 3,
        '+': 3,
        '?': 3,
        '.': 2,   # Concatenation
        '|': 1    # OR
    }

    output = []
    stack = []

    for token in regex:
        # Operand (a, b, c, 1, 2, etc.)
        if token.isalnum():
            output.append(token)

        # Left parenthesis
        elif token == '(':
            stack.append(token)

        # Right parenthesis
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '('

        # Operator
        else:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(token, 0):
                output.append(stack.pop())
            stack.append(token)

    # Pop remaining operators
    while stack:
        output.append(stack.pop())

    return "".join(output)


regex = input("Enter a REGEX: ")

formatted_regex = add_concatenation(regex)
postfix = regex_shunting_yard(formatted_regex)

print("With explicit concatenation:", formatted_regex)
print("Postfix (RPN):", postfix)
