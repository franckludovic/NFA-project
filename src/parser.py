# diane
<<<<<<< HEAD

def add_concatenation(regex):
    """Insert '.' between implicit concatenations (alternative to queen)."""
=======
def add_concatenation(regex):
    """
    Example: a.b|c -> ab.c|
    """
>>>>>>> 0ffa5b5a5805dd4d7d2142caaf24fde1d59a034e
    result = ""
    for i in range(len(regex)):
        c1 = regex[i]

<<<<<<< HEAD
        if i < len(regex) - 1:
            c2 = regex[i + 1]
            result += c1

            if (
                (c1.isalnum() or c1 in ")*+?")
                and
                (c2.isalnum() or c2 == '(')
            ):
                result += "."
=======
        if i + 1 < len(regex):
            c2 = regex[i + 1]

            result += c1

            # Conditions where concatenation is needed
            if (
                (c1.isalnum() or c1 in ")*+?") and
                (c2.isalnum() or c2 == '(')
            ):
                result += '.'
>>>>>>> 0ffa5b5a5805dd4d7d2142caaf24fde1d59a034e
        else:
            result += c1

    return result


def regex_shunting_yard(regex):
<<<<<<< HEAD
    """Convert regex (with explicit concatenation) to postfix using shunting yard."""

=======
    # Precedence rules for regex
>>>>>>> 0ffa5b5a5805dd4d7d2142caaf24fde1d59a034e
    precedence = {
        '*': 3,
        '+': 3,
        '?': 3,
<<<<<<< HEAD
        '.': 2,
        '&': 1,
        '|': 1
=======
        '.': 2,   # Concatenation
        '|': 1    # OR
>>>>>>> 0ffa5b5a5805dd4d7d2142caaf24fde1d59a034e
    }

    output = []
    stack = []

    for token in regex:
<<<<<<< HEAD

        if token.isalnum():
            output.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()   # remove '('

        else:  # operator
            while (
                stack
                and stack[-1] != "("
                and precedence.get(stack[-1], 0) >= precedence.get(token, 0)
            ):
                output.append(stack.pop())
            stack.append(token)

=======
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
>>>>>>> 0ffa5b5a5805dd4d7d2142caaf24fde1d59a034e
    while stack:
        output.append(stack.pop())

    return "".join(output)
<<<<<<< HEAD
=======


regex = input("Enter a REGEX: ")

formatted_regex = add_concatenation(regex)
postfix = regex_shunting_yard(formatted_regex)

print("With explicit concatenation:", formatted_regex)
print("Postfix (RPN):", postfix)
>>>>>>> 0ffa5b5a5805dd4d7d2142caaf24fde1d59a034e
