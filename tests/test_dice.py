# Test the Monopoly dice module.

import dice
import unittest             # My tests based on, https://docs.python.org/3/library/unittest.html


class TestDice(unittest.TestCase):

    # Roll the single die a lot of times, and check that it produces the expected set of values.
    def test_single_die(self):
        die_list = []
        for i in range(100000):
            die_list.append(dice.roll_a_die())
        self.assertEqual(set(die_list), {1, 2, 3, 4, 5, 6})

    # Roll two dice a lot of times, and check that it produced the expected set of values,
    # and also expected set of doubles.
    def test_two_dice(self):
        test_dice = dice.TwoDice()
        all_throws = []
        doubles = []

        for i in range(100000):
            test_throw = test_dice.roll()

            all_throws.append(test_throw)               # Build this list using the returned value.

            if test_dice.is_a_double:
                doubles.append(test_dice.this_throw)    # Build this list using this_throw attribute.

        self.assertEqual(set(all_throws), {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12})
        self.assertEqual(set(doubles), {2, 4, 6, 8, 10, 12})


if __name__ == '__main__':
    unittest.main()
