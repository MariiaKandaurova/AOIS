def expression_variables(expression):
    alphabet_set = []
    for individual_char in expression:
        if individual_char.isalpha() and individual_char not in alphabet_set:
            alphabet_set.append(individual_char)
    sorted_alphabet_set = sorted(alphabet_set)
    alphabet_set_list_length = len(sorted_alphabet_set)
    sub_parts = extract_sub_parts(expression)
    column_header = " ".join(sorted_alphabet_set) + " | " + " | ".join(sub_parts)
    print(column_header)
    for i in range(2**alphabet_set_list_length):
        number_collection = [(i >> j) & 1 for j in range(alphabet_set_list_length)]
        number_collection_str = " ".join(map(str, number_collection[::-1]))
        print(number_collection_str)


def extract_sub_parts(expression):
    data_stack = []
    sub_parts = []
    i = 0
    while i < len(expression):
        individual_char = expression[i]
        if individual_char == "(":
            data_stack.append(i)
        elif individual_char == ")":
            if data_stack:
                start = data_stack.pop()
                sub_parts.append(expression[start : i + 1])
        elif individual_char == "!":
            if i + 1 < len(expression) and (
                expression[i + 1] == " " or expression[i + 1].isalpha()
            ):
                j = i + 1
                while j < len(expression) and (
                    expression[j] == " " or expression[j].isalpha()
                ):
                    j += 1
                sub_parts.append(expression[i:j])
                i = j - 1
        i += 1
    if len(data_stack) == 1 and data_stack[0] == 0 and expression[-1] == ")":
        sub_parts.append(expression)
    print(sub_parts)
    return sub_parts


def to_reverse_polish(expression):
    precedence = {"!": 4, "&": 3, "|": 3, "~": 2, ">": 1}
    associative = {"!": "R", "&": "L", "|": "L", "~": "L", ">": "R"}
    output = []
    operators = []
    i = 0
    while i < len(expression):
        individual_char = expression[i]
        if individual_char.isalpha():
            output.append(individual_char)
        elif individual_char in precedence:
            while (
                operators
                and operators[-1] != "("
                and (
                    precedence[operators[-1]] > precedence[individual_char]
                    or (
                        precedence[operators[-1]] == precedence[individual_char]
                        and associative[individual_char] == "L"
                    )
                )
            ):
                output.append(operators.pop())
            operators.append(individual_char)
        elif individual_char == "(":
            operators.append(individual_char)
        elif individual_char == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()
        i += 1
    while operators:
        output.append(operators.pop())
    return " ".join(output)


def evaluate_expression(expression):
    reverse_polish = to_reverse_polish(expression)
    sorted_alphabet_set = sorted(set(filter(str.isalpha, expression)))
    alphabet_set_list_length = len(sorted_alphabet_set)
    outcome_vals = []

    for i in range(2**alphabet_set_list_length):
        number_collection = [(i >> j) & 1 for j in range(alphabet_set_list_length - 1, -1, -1)]
        value = evaluate_reverse_polish_expression(reverse_polish.split(), number_collection, sorted_alphabet_set)
        outcome_vals.append(value)

    return outcome_vals


def print_sub_parts(sub_parts, alphabet_set_list_length, sorted_alphabet_set):
    for i in range(2**alphabet_set_list_length):
        number_collection = [(i >> j) & 1 for j in range(alphabet_set_list_length)]
        number_collection_str = " ".join(map(str, number_collection[::-1]))
        print(number_collection_str, end=" | ")
        for subexp in sub_parts:
            value = extract_sub_parts(subexp, number_collection, sorted_alphabet_set)
            print(value, end=" | ")
        print()


def find_skcnf(expression):
    outcome_vals = evaluate_expression(expression)
    sorted_alphabet_set = sorted(set(filter(str.isalpha, expression)))
    alphabet_set_list_length = len(sorted_alphabet_set)
    skcnf = []
    for i, outcome_val in enumerate(outcome_vals):
        if outcome_val == 0:
            terms = []
            binary_number_collection = format(i, f"0{alphabet_set_list_length}b")
            for j, value in enumerate(binary_number_collection):
                if value == "1":
                    terms.append(f"!{sorted_alphabet_set[j]}")
                else:
                    terms.append(sorted_alphabet_set[j])
            skcnf.append(f"({' | '.join(terms)})")

    return " & ".join(skcnf) if skcnf else "1"


def find_sdnf_form(expression):
    outcome_vals = evaluate_expression(expression)
    sorted_alphabet_set = sorted(set(filter(str.isalpha, expression)))
    alphabet_set_list_length = len(sorted_alphabet_set)
    sdnf_form = []
    for i, outcome_val in enumerate(outcome_vals):
        if outcome_val == 1:
            terms = []
            binary_number_collection = format(i, f"0{alphabet_set_list_length}b")
            for j, value in enumerate(binary_number_collection):
                if value == "0":
                    terms.append(f"!{sorted_alphabet_set[j]}")
                else:
                    terms.append(sorted_alphabet_set[j])
            sdnf_form.append(f"({' & '.join(terms)})")

    return " | ".join(sdnf_form) if sdnf_form else "1"


def generate_truth_table(expression):
    sub_parts = extract_sub_parts(expression)
    reverse_polish = to_reverse_polish(expression)
    sorted_alphabet_set = sorted(set(expression) & set("abcdefghijklmnopqrstuvwxyz"))
    alphabet_set_list_length = len(sorted_alphabet_set)
    column_header = " ".join(sorted_alphabet_set) + " | " + " | ".join(sub_parts)
    print(column_header)

    for i in range(2**alphabet_set_list_length):
        number_collection = [(i >> j) & 1 for j in range(alphabet_set_list_length - 1, -1, -1)]
        number_collection_str = " ".join(map(str, number_collection))

        sub_number_collection = []
        for subexp in sub_parts:
            sub_reverse_polish = to_reverse_polish(subexp)
            value = evaluate_reverse_polish_expression(sub_reverse_polish, number_collection, sorted_alphabet_set)
            sub_number_collection.append(value)

        print(number_collection_str + " | " + " | ".join(map(str, sub_number_collection)))


def get_last_column_as_string(expression):
    sub_parts = extract_sub_parts(expression)
    reverse_polish = to_reverse_polish(expression)
    sorted_alphabet_set = sorted(set(expression) & set("abcdefghijklmnopqrstuvwxyz"))
    alphabet_set_list_length = len(sorted_alphabet_set)
    last_column = []

    for i in range(2**alphabet_set_list_length):
        number_collection = [(i >> j) & 1 for j in range(alphabet_set_list_length - 1, -1, -1)]
        sub_number_collection = []
        for subexp in sub_parts:
            sub_reverse_polish = to_reverse_polish(subexp)
            value = evaluate_reverse_polish_expression(sub_reverse_polish, number_collection, sorted_alphabet_set)
            sub_number_collection.append(value)
        last_column.append(str(sub_number_collection[-1]))

    return "".join(last_column)


def binary_to_decimal(binary_string):
    decimal_value = 0
    length = len(binary_string)
    for i in range(length):
        decimal_value += int(binary_string[i]) * (2 ** (length - i - 1))
    return decimal_value


def evaluate_reverse_polish_expression(reverse_polish, number_collection, sorted_alphabet_set):
    data_stack = []
    for token in reverse_polish:
        if token == "!":
            operand = data_stack.pop()
            outcome_val = int(not operand)
            data_stack.append(outcome_val)
        elif token in ["&", "|", "~", ">"]:
            b = data_stack.pop()
            a = data_stack.pop()
            if token == "&":
                outcome_val = a & b
            elif token == "|":
                outcome_val = a | b
            elif token == "~":
                outcome_val = int((a and b) or (not a and not b))
            elif token == ">":
                outcome_val = int((not a) or b)
            data_stack.append(outcome_val)
        elif token.isalpha():
            if token in sorted_alphabet_set:
                index = sorted_alphabet_set.index(token)
                data_stack.append(number_collection[index])
            else:
                raise ValueError(
                    f"Unexpected token '{token}' not found in sorted_alphabet_set"
                )
    return data_stack.pop() if data_stack else 0


if __name__ == "__main__":
    expression = "(a|(b&(!c)))"
    generate_truth_table(expression)
    print("СКНФ", find_skcnf(expression))
    print("СДНФ", find_sdnf_form(expression))

    last_column_string = get_last_column_as_string(expression)
    print("Индексная форма:\n", last_column_string)

    decimal_value = binary_to_decimal(last_column_string)
    print("Перевод:\n", decimal_value)
