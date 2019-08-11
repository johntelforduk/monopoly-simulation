# Run unit tests on various modules.

import dice
import board
import unittest                                 # My tests based on, https://docs.python.org/3/library/unittest.html


class TestDice(unittest.TestCase):

    # Roll the single die a lot of times, and check that it produces the expected set of values.
    def test_single_die(self):
        test_die = dice.TwoDice()
        die_list = []

        for i in range(100000):
            die_list.append(test_die.roll_one_die())
        self.assertEqual(set(die_list), {1, 2, 3, 4, 5, 6})

    # Roll two dice a lot of times, and check that it produced the expected set of values,
    # and also expected set of doubles.
    def test_two_dice(self):
        test_dice = dice.TwoDice()
        all_throws = []
        doubles = []

        for i in range(100000):
            test_throw = test_dice.roll_two_dice()

            all_throws.append(test_throw)               # Build this list using the returned value.

            if test_dice.is_a_double:
                doubles.append(test_dice.this_throw)    # Build this list using this_throw attribute.

        self.assertEqual(set(all_throws), {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12})
        self.assertEqual(set(doubles), {2, 4, 6, 8, 10, 12})


class TestBoard(unittest.TestCase):

    def test_move_backwards_and_forwards(self):
        test_board = board.Board()

        # Square 0 should be Go.
        curr_square = 0
        self.assertEqual(test_board.squares[curr_square].name, 'Go')

        # 3 squares forwards from Go should be Whitechapel Road.
        curr_square = test_board.forwards(curr_square, 3)
        self.assertEqual(test_board.squares[curr_square].name, 'Whitechapel Road')

        # 2 squares backwards from Whitechapel Road should be Old Kent Road.
        curr_square = test_board.backwards(curr_square, 2)
        self.assertEqual(test_board.squares[curr_square].name, 'Old Kent Road')

        # 2 squares backwards from Old Kent Road should be Mayfair.
        curr_square = test_board.backwards(curr_square, 2)
        self.assertEqual(test_board.squares[curr_square].name, 'Mayfair')

        # 4 squares backwards from Mayfair should be Liverpool Street Station.
        curr_square = test_board.backwards(curr_square, 4)
        self.assertEqual(test_board.squares[curr_square].name, 'Liverpool Street Station')

        # 9 squares forwards from Liverpool Street Station should be Income Tax (pay £200).
        curr_square = test_board.forwards(curr_square, 9)
        self.assertEqual(test_board.squares[curr_square].name, 'Income Tax (pay £200)')

        # 4 squares backwards from Income Tax (pay £200) should be Go.
        curr_square = test_board.backwards(curr_square, 4)
        self.assertEqual(test_board.squares[curr_square].name, 'Go')

    def test_find_square(self):
        test_board = board.Board()

        self.assertEqual(test_board.find_square('Go'), 0)
        self.assertEqual(test_board.find_square('Jail'), 10)
        self.assertEqual(test_board.find_square('Marlborough Street'), 18)
        self.assertEqual(test_board.find_square('Mayfair'), 39)

        # There is no square as Nowhere Road, so should return None.
        self.assertEqual(test_board.find_square('Nowhere Road'), None)


if __name__ == '__main__':
    unittest.main()
