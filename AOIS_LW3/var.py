class Variable:
    def __init__(self, positive: bool, char: str):
        self.positive: bool = positive
        self.char: str = char

    def __str__(self):
        return self.char if self.positive else "!" + self.char

    def copy(self):
        return Variable(self.positive, self.char)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.char == other.char and self.positive == other.positive


area_sizes = [
    [1, 8], [8, 1], [4, 4], [2, 4], [4, 2], [2, 2],
    [1, 4], [4, 1], [1, 2], [2, 1], [1, 1],
]


class Form:
    def __init__(self):
        self.expr_form = []

    def __str__(self):
        return " ".join(str(elem) for elem in self.expr_form)

    def __getitem__(self, key):
        return self.expr_form[key]

    def __setitem__(self, key, value):
        self.expr_form[key] = value

    def append_form(self, var: Variable):
        self.expr_form.append(var)

    def get_length(self):
        return len(self.expr_form)

    def is_compatible(self, other):
        if self.get_length() != other.get_length():
            return False, None

        identic_counter = 0
        partially_identic_counter = 0
        partially_char = None

        for elem in self.expr_form:
            for other_elem in other.expr_form:
                if elem.char == other_elem.char:
                    if elem.positive == other_elem.positive:
                        identic_counter += 1
                    else:
                        partially_identic_counter += 1
                        partially_char = elem.char

        if partially_identic_counter != 1 or identic_counter != len(self.expr_form) - 1:
            return False, None

        new_form = Form()
        for elem in self.expr_form:
            if elem.char != partially_char:
                new_form.append_form(elem.copy())

        return True, new_form

    def is_other_contained(self, other):
        for other_elem in other.expr_form:
            if not any(
                elem.char == other_elem.char and elem.positive == other_elem.positive
                for elem in self.expr_form
            ):
                return False
        return True


def get_str_from_form(form, char):
    return "".join(str(elem) + char for elem in form)[:-1]


def get_str_from_full_form(full_form, char):
    char_in = "&" if char == "|" else "|"
    return char.join(f"({get_str_from_form(form, char_in)})" for form in full_form)
