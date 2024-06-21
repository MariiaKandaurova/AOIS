import re
from KMap import KMap
from table import Table
from var import *


def calc_SDNF_algorithmic(expression_str: str):
    return _calc_algorithmic_method(expression_str, "SDNF", "|", True)


def calc_SKNF_algorithmic(expression_str: str):
    return _calc_algorithmic_method(expression_str, "SKNF", "&", False)


def _calc_algorithmic_method(expression_str, form_type, operator, is_sdnf):
    table = Table(expression_str)
    result_form = _get_form_from_string(getattr(table, f"calc_{form_type}")())

    print(get_str_from_full_form(result_form, operator))
    result_form = reduce_full_form(result_form)
    print(get_str_from_full_form(result_form, operator))
    result_form = reduce_form_algorihtmic_method(result_form, is_sdnf)

    return get_str_from_full_form(result_form, operator)


def calc_SDNF_table_method(expression_str: str):
    return _calc_table_method(expression_str, "SDNF", "|")


def calc_SKNF_table_method(expression_str: str):
    return _calc_table_method(expression_str, "SKNF", "&")


def _calc_table_method(expr_str, form_type, operator):
    table = Table(expr_str)
    full_form = _get_form_from_string(getattr(table, f"calc_{form_type}")())

    print(get_str_from_full_form(full_form, operator))
    reduced_form = reduce_full_form(full_form)

    print("Before: ")
    print_minimized_table(full_form, reduced_form, operator)
    reduced_form = form_table_reduction(full_form, reduced_form, operator)
    print("After: ")
    print_minimized_table(full_form, reduced_form, operator)

    return get_str_from_full_form(reduced_form, operator)


def calc_SDNF_Karno_method(expr_str: str):
    return _calc_karno_method(expr_str, "SDNF")


def calc_SKNF_Karno_method(expr_str: str):
    return _calc_karno_method(expr_str, "SKNF")


def _calc_karno_method(expr_str, form_type):
    table = Table(expr_str)
    map = KMap(table.get_internal_table(), table.get_vars())
    map.print_map()
    return getattr(map, f"calc_{form_type}")()


def print_minimized_table(full_form, reduced_form, char):
    char_in = "&" if char == "|" else "|"
    header = "".join(f"{get_str_from_form(form, char_in):<10}" for form in full_form)

    print(f"{'':<10}{header}")
    for form in reduced_form:
        row = "".join(
            f"{'x' if form_full.is_other_contained(form) else ' ' :<10}"
            for form_full in full_form
        )
        print(f"{get_str_from_form(form, char_in):<10}{row}")


def form_table_reduction(full_form, reduced_form, char):
    table = [
        [full_elem.is_other_contained(reduced_elem) for full_elem in full_form]
        for reduced_elem in reduced_form
    ]

    i = 0
    while i < len(table):
        if all(
            any(table[k][j] for k in range(len(table)) if i != k)
            for j in range(len(table[i]))
        ):
            table.pop(i)
            reduced_form.pop(i)
            i -= 1
        i += 1
    return reduced_form


def reduce_form_algorihtmic_method(full_form, equal_cond):
    reduced = False
    while not reduced:
        reduced = True
        ind = 0
        while ind < len(full_form):
            if is_unnecessary(full_form, ind, equal_cond):
                full_form.pop(ind)
                reduced = False
            else:
                ind += 1
    return full_form


def is_unnecessary(full_form, ind, equal_cond):
    part = full_form[ind]
    solution = {}
    for elem in part:
        if elem.positive == equal_cond:
            solution[elem.char] = True
        else:
            solution[elem.char] = False

    for i in range(len(full_form)):
        if i == ind:
            continue

        for elem in full_form[i]:
            if solution.get(elem.char) is None:
                continue

            cond = not (solution[elem.char] != elem.positive)
            if cond:
                if cond == equal_cond:
                    return True
            else:
                if cond != equal_cond:
                    return True

    return False


def reduce_full_form(full_form):
    reduced = True
    while reduced:
        reduced = False
        new_forms = []
        to_delete = set()
        for i in range(len(full_form)):
            for j in range(i + 1, len(full_form)):
                is_reduced, new_form = full_form[i].is_compatible(full_form[j])
                if is_reduced:
                    new_forms.append(new_form)
                    to_delete.update([i, j])
                    reduced = True

        full_form = [
            el for ind, el in enumerate(full_form) if ind not in to_delete
        ] + new_forms
    return full_form


def _get_form_from_string(shortened_form: str):
    result = []
    for bracket in re.findall(r"\((.*?)\)", shortened_form):
        form_bracket = Form()
        positive = True
        for char in bracket:
            if char == "!":
                positive = False
            elif char not in "&|":
                form_bracket.append_form(Variable(positive, char))
                positive = True
        result.append(form_bracket)

    return result
