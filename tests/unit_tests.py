# Run unit tests on various modules.

import dice
import board
import cards
import player
import game
import unittest                                 # These tests based on, https://docs.python.org/3/library/unittest.html


class TestDice(unittest.TestCase):

    # Roll the single die a lot of times, and check that it produces the expected set of values.
    def test_single_die(self):
        test_die = dice.TwoDice()
        die_list = []

        for i in range(10000):
            die_list.append(test_die.roll_one_die())
        self.assertEqual(set(die_list), {1, 2, 3, 4, 5, 6})

    # Roll two dice a lot of times, and check that it produced the expected set of values,
    # and also expected set of doubles.
    def test_two_dice(self):
        test_dice = dice.TwoDice()
        all_throws = []
        doubles = []

        for i in range(10000):
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

        # Test some colour group sizes.
        self.assertEqual(test_board.colour_group_size['Brown'], 2)
        self.assertEqual(test_board.colour_group_size['Orange'], 3)
        self.assertEqual(test_board.colour_group_size['Yellow'], 3)
        self.assertEqual(test_board.colour_group_size['Dark Blue'], 2)

    def test_find_square(self):
        test_board = board.Board()

        self.assertEqual(test_board.find_square('Go'), 0)
        self.assertEqual(test_board.find_square('Jail'), 10)
        self.assertEqual(test_board.find_square('Marlborough Street'), 18)
        self.assertEqual(test_board.find_square('Mayfair'), 39)

        # There is no square as Nowhere Road, so should return None.
        self.assertEqual(test_board.find_square('Nowhere Road'), None)


class TestCards(unittest.TestCase):

    def test_chance_pack(self):

        test_chance = cards.CardPack('Chance', 'chance_cards.csv')
        test_board = board.Board()

        for c in test_chance.pack:

            # advance_to should be a square on the board for Advance cards.
            if c.category == 'Advance':
                self.assertEqual(test_board.find_square(c.advance_to) is not None, True)

            # money_amount should not be zero for Money card.
            elif c.category == 'Money':
                self.assertEqual(c.money_amount != 0, True)

    def test_community_chest_pack(self):

        test_community_chest = cards.CardPack('Community Chest', 'community_chest_cards.csv')
        test_board = board.Board()

        for c in test_community_chest.pack:

            # advance_to should be a square on the board for Advance cards.
            if c.category == 'Advance':
                self.assertEqual(test_board.find_square(c.advance_to) is not None, True)

            # money_amount should not be zero for Money card.
            elif c.category == 'Money':
                self.assertEqual(c.money_amount != 0, True)

        # There should be 16 Community Chest cards.
        self.assertEqual(len(test_community_chest.pack), 16)

    def test_take_card(self):
        test_chance = cards.CardPack('Chance', 'chance_cards.csv')

        # There should be 16 Chance cards.
        self.assertEqual(len(test_chance.pack), 16)

        # The top card in fresh Chance pack should be Go.
        this_card = test_chance.take_card()
        self.assertEqual(this_card.card_name, 'Advance to Go')

        # Now there should be 15 Chance cards.
        self.assertEqual(len(test_chance.pack), 15)

        # Put the card back in the (bottom) of the pack.
        test_chance.add_card(this_card)

        # Now there should be 16 Chance cards again.
        self.assertEqual(len(test_chance.pack), 16)

        # The top card should now be Go To Jail.
        this_card = test_chance.take_card()
        self.assertEqual(this_card.card_name[0:11], 'Go to jail.')


class TestPlayer(unittest.TestCase):

    def test_player(self):

        test_player = player.Player()

        # Test that default values for some attributes are correct for newly created player.
        self.assertEqual(test_player.money, 1500)
        self.assertEqual(test_player.in_jail, False)
        self.assertEqual(test_player.deeds, [])


class TestGame(unittest.TestCase):

    def test_game(self):

        test_game = game.Game(4, False)     # 4 players, non-verbose mode.

        # The stats lists should have same number of elements as there are square on the board.
        self.assertEqual(len(test_game.land_on_frequency), len(test_game.board.squares))
        self.assertEqual(len(test_game.turn_end_frequency), len(test_game.board.squares))

        # There should be 4 player objects in the players list.
        self.assertEqual(len(test_game.players), 4)


if __name__ == '__main__':
    unittest.main()
