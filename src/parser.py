# diane

def add_concatenation(regex):
    """Insert '.' between implicit concatenations (alternative to queen)."""
    result = ""
    for i in range(len(regex)):
        c1 = regex[i]

        if i < len(regex) - 1:
            c2 = regex[i + 1]
            result += c1

            if (
                (c1.isalnum() or c1 in ")*+?")
                and
                (c2.isalnum() or c2 == '(')
            ):
                result += "."
        else:
            result += c1

    return result


def regex_shunting_yard(regex):
    """Convert regex (with explicit concatenation) to postfix using shunting yard."""

    precedence = {
        '*': 3,
        '+': 3,
        '?': 3,
        '.': 2,
        '&': 1,
        '|': 1
    }

    output = []
    stack = []

    for token in regex:

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

    while stack:
        output.append(stack.pop())

    return "".join(output)
