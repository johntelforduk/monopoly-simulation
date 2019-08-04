# Test the Monopoly board module.

import board
import unittest             # My tests based on, https://docs.python.org/3/library/unittest.html


class TestBoard(unittest.TestCase):

    def test_move_forward(self):
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


if __name__ == '__main__':
    unittest.main()
