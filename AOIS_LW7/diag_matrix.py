def create_matrix():
    matrix = [[False for _ in range(16)] for _ in range(16)]
    for i in range(16):
        matrix[i][i] = True

    return matrix


def print_matrix(matrix):
    for i in range(16):
        for j in range(16):
            print(int(matrix[i][j]), end=" ")
        print()


def get_el(matrix, i, j):
    return matrix[(i + j) % 16][i % 16]


def set_el(matrix, i, j, val):
    matrix[(i + j) % 16][i % 16] = val


def get_word(matrix, i):
    res = ""
    for j in range(16):
        res += str(int(get_el(matrix, i, j)))
    return res


def set_word(matrix, i, word):
    for j in range(16):
        set_el(matrix, i, j, bool(int(word[j])))


def get_diag_word(matrix, i):
    res = ""
    for j in range(16):
        res += str(int(get_el(matrix, j, i)))
    return res


def set_diag_word(matrix, i, word):
    for j in range(16):
        set_el(matrix, j, i, bool(int(word[j])))


def second_op(matrix, first, second, third):
    for i in range(16):
        second_el = get_el(matrix, i, second)
        set_el(matrix, i, third, second_el)


def inv_second_op(matrix, first, second, third):
    for i in range(16):
        second_el = get_el(matrix, i, second)
        second_el = not second_el
        set_el(matrix, i, third, second_el)


def const_one(matrix, first, second, third):
    for i in range(16):
        set_el(matrix, i, third, True)


def const_zero(matrix, first, second, third):
    for i in range(16):
        set_el(matrix, i, third, False)


def AB_task(matrix, start_values: str):
    if len(start_values) == 3:
        for x in range(16):
            if any(
                bool(int(start_values[i])) != get_el(matrix, x, i) for i in range(3)
            ):
                continue

            sum_word_fields(matrix, x)


def sum_word_fields(matrix, word_ind):
    word = get_word(matrix, word_ind)
    field = ""
    overflow = False
    for i in range(4):
        if word[6 - i] == "1" and word[10 - i] == "1":
            if overflow:
                field += "1"
            else:
                field += "0"
                overflow = True
        elif word[6 - i] == "1" or word[10 - i] == "1":
            if overflow:
                field += "0"
            else:
                field += "1"
        else:
            if overflow:
                field += "1"
                overflow = False
            else:
                field += "0"
    if overflow:
        field += "1"
    else:
        field += "0"
    res = word[:11] + field[::-1]
    set_word(matrix, word_ind, res)


def match_search(matrix, word):
    max_match_count = 0
    max_match_word = get_word(matrix, 0)
    max_ind = 0
    if len(word) == 16:
        for i in range(0, 16):
            l_var = not bool(int(word[i])) and bool(int(max_match_word[i]))
            g_var = bool(int(word[i])) and not bool(int(max_match_word[i]))
            if g_var == l_var:
                max_match_count += 1

        for i in range(1, 16):
            test_word = get_word(matrix, i)
            matching_count = 0
            for j in range(0, 16):
                l_var = not bool(int(word[i])) and bool(int(max_match_word[i]))
                g_var = bool(int(word[i])) and not bool(int(max_match_word[i]))
                if g_var == l_var:
                    matching_count += 1

            if matching_count > max_match_count:
                max_match_count = matching_count
                max_match_word = test_word
                max_ind = i

        return (max_ind, max_match_word)
    return "Invalid word size"
