import unittest
from diag_matrix import *


class testMatrix(unittest.TestCase):
    def setUp(self):
        self.m = create_matrix()

    def test_get_el(self):
        self.assertEqual(True, get_el(self.m, 0, 0))

    def test_set_el(self):
        set_el(self.m, 0, 0, False)
        self.assertEqual(False, get_el(self.m, 0, 0))

    def test_set_word(self):
        set_word(self.m, 2, "1011100110001011")
        self.assertEqual("1011100110001011", get_word(self.m, 2))

    def test_second_op(self):
        set_word(self.m, 2, "1011100110001011")
        second_op(self.m, 2, 4, 5)
        self.assertEqual("0010000000000000", get_diag_word(self.m, 4))

    def test_inv_second_op(self):
        set_word(self.m, 2, "1011100110001011")
        inv_second_op(self.m, 2, 4, 4)
        self.assertEqual("1101111111111111", get_diag_word(self.m, 4))

    def test_const_one(self):
        const_one(self.m, 2, 3, 1)
        set_word(self.m, 2, "1011100110001011")
        self.assertEqual("1101111111111111", get_diag_word(self.m, 1))

    def test_const_zero(self):
        const_zero(self.m, 2, 3, 0)
        set_word(self.m, 2, "1011100110001011")
        self.assertEqual("0010000000000000", get_diag_word(self.m, 0))

    def test_AB_task(self):
        second_op(self.m, 1, 0, 3)
        second_op(self.m, 1, 0, 9)
        const_one(self.m, 1, 0, 6)
        const_one(self.m, 1, 0, 10)
        set_el(self.m, 3, 15, True)
        set_el(self.m, 3, 13, True)
        AB_task(self.m, "100")
        self.assertEqual("1001001001101100", get_word(self.m, 0))

    def test_match_search(self):
        second_op(self.m, 1, 0, 3)
        second_op(self.m, 1, 0, 9)
        const_one(self.m, 1, 0, 6)
        const_one(self.m, 1, 0, 10)
        set_el(self.m, 3, 15, True)
        set_el(self.m, 3, 13, True)
        AB_task(self.m, "100")
        self.assertEqual(
            (3, "1001001001101100"), match_search(self.m, "1111111111111111")
        )


if __name__ == "__main__":
    unittest.main()
