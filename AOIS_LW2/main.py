def expression_variables(expression):
    letters = []
    for char in expression:
        if char.isalpha() and char not in letters:
            letters.append(char)
    sorted_letters = sorted(letters)
    letters_list_length = len(sorted_letters)
    subexpressions = extract_subexpressions(expression)
    header = " ".join(sorted_letters) + " | " + " | ".join(subexpressions)
    print(header)
    for i in range(2**letters_list_length):
        values = [(i >> j) & 1 for j in range(letters_list_length)]
        values_str = " ".join(map(str, values[::-1]))
        print(values_str)


def extract_subexpressions(expression):
    stack = []
    subexpressions = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char == "(":
            stack.append(i)
        elif char == ")":
            if stack:
                start = stack.pop()
                subexpressions.append(expression[start : i + 1])
        elif char == "!":
            if i + 1 < len(expression) and (
                expression[i + 1] == " " or expression[i + 1].isalpha()
            ):
                j = i + 1
                while j < len(expression) and (
                    expression[j] == " " or expression[j].isalpha()
                ):
                    j += 1
                subexpressions.append(expression[i:j])
                i = j - 1
        i += 1
    if len(stack) == 1 and stack[0] == 0 and expression[-1] == ")":
        subexpressions.append(expression)
    print(subexpressions)
    return subexpressions


def to_rpn(expression):
    precedence = {"!": 4, "&": 3, "|": 3, "~": 2, ">": 1}
    associative = {"!": "R", "&": "L", "|": "L", "~": "L", ">": "R"}
    output = []
    operators = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isalpha():
            output.append(char)
        elif char in precedence:
            while (
                operators
                and operators[-1] != "("
                and (
                    precedence[operators[-1]] > precedence[char]
                    or (
                        precedence[operators[-1]] == precedence[char]
                        and associative[char] == "L"
                    )
                )
            ):
                output.append(operators.pop())
            operators.append(char)
        elif char == "(":
            operators.append(char)
        elif char == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()
        i += 1
    while operators:
        output.append(operators.pop())
    return " ".join(output)


def evaluate_expression(expression):
    rpn = to_rpn(expression)
    sorted_letters = sorted(set(filter(str.isalpha, expression)))
    letters_list_length = len(sorted_letters)
    results = []

    for i in range(2**letters_list_length):
        values = [(i >> j) & 1 for j in range(letters_list_length - 1, -1, -1)]
        value = evaluate_rpn_expression(rpn.split(), values, sorted_letters)
        results.append(value)

    return results


def print_subexpressions(subexpressions, letters_list_length, sorted_letters):
    for i in range(2**letters_list_length):
        values = [(i >> j) & 1 for j in range(letters_list_length)]
        values_str = " ".join(map(str, values[::-1]))
        print(values_str, end=" | ")
        for subexp in subexpressions:
            value = extract_subexpressions(subexp, values, sorted_letters)
            print(value, end=" | ")
        print()


def find_skcnf(expression):
    results = evaluate_expression(expression)
    sorted_letters = sorted(set(filter(str.isalpha, expression)))
    letters_list_length = len(sorted_letters)
    skcnf = []
    for i, result in enumerate(results):
        if result == 0:
            terms = []
            binary_values = format(i, f"0{letters_list_length}b")
            for j, value in enumerate(binary_values):
                if value == "1":
                    terms.append(f"!{sorted_letters[j]}")
                else:
                    terms.append(sorted_letters[j])
            skcnf.append(f"({' | '.join(terms)})")

    return " & ".join(skcnf) if skcnf else "1"


def find_sdnf(expression):
    results = evaluate_expression(expression)
    sorted_letters = sorted(set(filter(str.isalpha, expression)))
    letters_list_length = len(sorted_letters)
    sdnf = []
    for i, result in enumerate(results):
        if result == 1:
            terms = []
            binary_values = format(i, f"0{letters_list_length}b")
            for j, value in enumerate(binary_values):
                if value == "0":
                    terms.append(f"!{sorted_letters[j]}")
                else:
                    terms.append(sorted_letters[j])
            sdnf.append(f"({' & '.join(terms)})")

    return " | ".join(sdnf) if sdnf else "1"


def generate_truth_table(expression):
    subexpressions = extract_subexpressions(expression)
    rpn = to_rpn(expression)
    sorted_letters = sorted(set(expression) & set("abcdefghijklmnopqrstuvwxyz"))
    letters_list_length = len(sorted_letters)
    header = " ".join(sorted_letters) + " | " + " | ".join(subexpressions)
    print(header)

    for i in range(2**letters_list_length):
        values = [(i >> j) & 1 for j in range(letters_list_length - 1, -1, -1)]
        values_str = " ".join(map(str, values))

        sub_values = []
        for subexp in subexpressions:
            sub_rpn = to_rpn(subexp)
            value = evaluate_rpn_expression(sub_rpn, values, sorted_letters)
            sub_values.append(value)

        print(values_str + " | " + " | ".join(map(str, sub_values)))


def get_last_column_as_string(expression):
    subexpressions = extract_subexpressions(expression)
    rpn = to_rpn(expression)
    sorted_letters = sorted(set(expression) & set("abcdefghijklmnopqrstuvwxyz"))
    letters_list_length = len(sorted_letters)
    last_column = []

    for i in range(2**letters_list_length):
        values = [(i >> j) & 1 for j in range(letters_list_length - 1, -1, -1)]
        sub_values = []
        for subexp in subexpressions:
            sub_rpn = to_rpn(subexp)
            value = evaluate_rpn_expression(sub_rpn, values, sorted_letters)
            sub_values.append(value)
        last_column.append(str(sub_values[-1]))

    return "".join(last_column)


def binary_to_decimal(binary_string):
    decimal_value = 0
    length = len(binary_string)
    for i in range(length):
        decimal_value += int(binary_string[i]) * (2 ** (length - i - 1))
    return decimal_value


def evaluate_rpn_expression(rpn, values, sorted_letters):
    stack = []
    for token in rpn:
        if token == "!":
            operand = stack.pop()
            result = int(not operand)
            stack.append(result)
        elif token in ["&", "|", "~", ">"]:
            b = stack.pop()
            a = stack.pop()
            if token == "&":
                result = a & b
            elif token == "|":
                result = a | b
            elif token == "~":
                result = int((a and b) or (not a and not b))
            elif token == ">":
                result = int((not a) or b)
            stack.append(result)
        elif token.isalpha():
            if token in sorted_letters:
                index = sorted_letters.index(token)
                stack.append(values[index])
            else:
                raise ValueError(
                    f"Unexpected token '{token}' not found in sorted_letters"
                )
    return stack.pop() if stack else 0


if __name__ == "__main__":
    expression = "(a|(b&(!c)))"
    generate_truth_table(expression)
    print("СКНФ", find_skcnf(expression))
    print("СДНФ", find_sdnf(expression))

    last_column_string = get_last_column_as_string(expression)
    print("Индексная форма:\n", last_column_string)

    decimal_value = binary_to_decimal(last_column_string)
    print("Перевод:\n", decimal_value)
