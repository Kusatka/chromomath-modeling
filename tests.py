import unittest
from visualize.hmm_module import ker, model_ker_sum_squares, model_ker_sum_cubes

class TestHmmModule(unittest.TestCase):
    def test_ker_single_digit(self):
        self.assertEqual(ker(5), 5)

    def test_ker_two_digits(self):
        self.assertEqual(ker(38), 2)

    def test_ker_large_number(self):
        self.assertEqual(ker(999), 9)

    def test_ker_zero(self):
        self.assertEqual(ker(0), 0)

    def test_ker_negative(self):
        self.assertEqual(ker(-10), 0)

    def test_model_ker_sum_squares(self):
        self.assertEqual(model_ker_sum_squares(3, 4), ker(9 + 16))  # 25 -> 7

    def test_model_ker_sum_cubes(self):
        self.assertEqual(model_ker_sum_cubes(1, 2), ker(1 + 8))  # 9 -> 9

if __name__ == '__main__':
    unittest.main()