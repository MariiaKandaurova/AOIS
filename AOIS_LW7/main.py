from diag_matrix import *

if __name__ == "__main__":
    m = create_matrix()

    print_matrix(m)
    second_op(m, 1, 0, 3)
    second_op(m, 1, 0, 9)
    const_one(m, 1, 0, 6)
    const_one(m, 1, 0, 10)
    set_el(m, 3, 15, True)
    set_el(m, 3, 13, True)
    print()
    print_matrix(m)
    print()
    AB_task(m, "100")
    set_word(m, 2, "1011100110001011")

    print_matrix(m)
