# queen

def insert_concatenation_operator(regex: str) -> str:
    """
    Takes a raw regex string and inserts '.' wherever an implicit
    concatenation should occur.
    """

    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789()*+?|.")

    # Validate characters
    for char in regex:
        if char not in allowed_chars:
            raise ValueError(f"Invalid character detected: '{char}'")

    # Invalid start characters
    if regex[0] in "*?|)":
        raise ValueError("Regex cannot start with '*', '?', '|', or ')'.")

    # Invalid ending characters
    if regex[-1] in "|(":
        raise ValueError("Regex cannot end with '|' or '('.")

    # Edge case: too short
    if len(regex) < 2:
        return regex

    result = ""
    symbols = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    for i in range(len(regex) - 1):
        c1 = regex[i]
        c2 = regex[i + 1]

        result += c1

        # Check for concatenation
        if (
            (c1 in symbols or c1 in ")*+?")
            and
            (c2 in symbols or c2 == '(')
        ):
            result += "."

    result += regex[-1]
    return result
