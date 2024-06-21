import math
import itertools


class Table:
    def __init__(self, expression: str):
        variables = {}
        self.operations = ["&", "!", "|", "-", "~", "(", ")"]
        rpn: str = self._get_RPN(expression, variables)

        table = []
        l_values = [False, True]
        all_permutations = [
            list(i) for i in itertools.product(l_values, repeat=len(variables))
        ]
        for permutation in all_permutations:
            for ind, variable in enumerate(variables):
                variables[variable] = permutation[ind]

            table.append(permutation)
            table[-1].append(self._calc_rpn(rpn, variables))
        self.variables = list(variables.keys())
        self.table = table

    def get_vars(self):
        return self.variables

    def get_internal_table(self):
        return self.table

    def print_table(self):
        headers = " ".join(f"{variable:<3}" for variable in self.variables + ["res"])
        print(headers)
        for row in self.table:
            formatted_row = " ".join(f"{1 if elem else 0:<3}" for elem in row)
            print(formatted_row)

    def calc_SDNF(self):
        result = ""
        for row in self.table:
            if row[-1]:
                result += (
                    "("
                    + "".join(
                        f"{'!' if not elem else ''}{var}&"
                        for var, elem in zip(self.variables, row[:-1])
                    ).rstrip("&")
                    + ")|"
                )
        return result.rstrip("|")

    def calc_SKNF(self):
        result = ""
        for row in self.table:
            if not row[-1]:
                result += (
                    "("
                    + "".join(
                        f"{'!' if elem else ''}{var}|"
                        for var, elem in zip(self.variables, row[:-1])
                    ).rstrip("|")
                    + ")&"
                )
        return result.rstrip("&")

    def calc_number_form(self):
        conjuctions = [str(ind) for ind, row in enumerate(self.table) if not row[-1]]
        disjunctions = [str(ind) for ind, row in enumerate(self.table) if row[-1]]
        return f"({', '.join(conjuctions)}) /\\\n({', '.join(disjunctions)}) \\/"

    def calc_form_index(self):
        binary_string = "".join("1" if row[-1] else "0" for row in self.table)
        return sum(
            int(char) * math.pow(2, ind)
            for ind, char in enumerate(reversed(binary_string))
        )

    def _get_RPN(self, expression: str, variables) -> str:
        priority = {"!": 3, "&": 2, "|": 1, "-": 0, "~": 0, "(": -1, ")": 0}
        li = []
        result = ""
        for char in expression:
            if char == ">" or char == " ":
                continue

            if char in self.operations:
                if char == "(":
                    li.append(char)
                else:
                    while li and priority[li[-1]] >= priority[char]:
                        result += li.pop()

                    if char == ")":
                        li.pop()
                    else:
                        li.append(char)
            else:
                variables[char] = False
                result += char
        while li:
            char = li.pop()
            result += char
            if char not in self.operations:
                variables[char] = False
        return result

    def _do_binary(self, r, l, operation) -> bool:
        if operation == "&":
            return r & l
        elif operation == "|":
            return r | l
        elif operation == "-":
            return (not r) | l
        elif operation == "~":
            return r == l

    def _get_bool(self, st, vars) -> bool:
        element = st.pop()
        if element is not False and element is not True:
            return vars[element]
        return element

    def _calc_rpn(self, rpn: str, vars) -> bool:
        stack = []
        for curChar in rpn:
            if curChar not in self.operations:
                stack.append(curChar)

            else:
                if curChar == "!":
                    var = stack.pop()
                    if var is not False and var is not True:
                        res = vars[var]
                    else:
                        res = var
                    stack.append(not res)
                else:
                    left = self._get_bool(stack, vars)
                    right = self._get_bool(stack, vars)
                    stack.append(self._do_binary(right, left, curChar))

        return stack.pop()
