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
        self.assertEqual(test_board.index_to_square_name(curr_square), 'Go')

        # 3 squares forwards from Go should be Whitechapel Road.
        curr_square = test_board.forwards(curr_square, 3)
        self.assertEqual(test_board.index_to_square_name(curr_square), 'Whitechapel Road')

        # 2 squares backwards from Whitechapel Road should be Old Kent Road.
        curr_square = test_board.backwards(curr_square, 2)
        self.assertEqual(test_board.index_to_square_name(curr_square), 'Old Kent Road')

        # 2 squares backwards from Old Kent Road should be Mayfair.
        curr_square = test_board.backwards(curr_square, 2)
        self.assertEqual(test_board.index_to_square_name(curr_square), 'Mayfair')

        # 4 squares backwards from Mayfair should be Liverpool Street Station.
        curr_square = test_board.backwards(curr_square, 4)
        self.assertEqual(test_board.index_to_square_name(curr_square), 'Liverpool Street Station')

        # 9 squares forwards from Liverpool Street Station should be Income Tax (pay £200).
        curr_square = test_board.forwards(curr_square, 9)
        self.assertEqual(test_board.index_to_square_name(curr_square), 'Income Tax (pay £200)')

        # 4 squares backwards from Income Tax (pay £200) should be Go.
        curr_square = test_board.backwards(curr_square, 4)
        self.assertEqual(test_board.index_to_square_name(curr_square), 'Go')

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

    def test_card_packs(self):

        test_board = board.Board()
        test_chance = cards.ChancePack(shuffle_it=True)
        test_community_chest = cards.CommunityChestPack(shuffle_it=True)

        for pack in [test_chance.pack, test_community_chest.pack]:  # Test both of the card packs.

            self.assertEqual(len(pack), 16)                         # There should be 16 cards in each pack.

            for card in pack:                                       # Test each card in each pack.

                # advance_to should be a square on the board for Advance cards.
                if card.category == 'Advance':
                    self.assertEqual(test_board.find_square(card.advance_to) is not None, True)

                # money_amount should not be zero for Money card.
                elif card.category == 'Money':
                    self.assertEqual(card.money_amount != 0, True)

    def test_take_card(self):
        test_chance = cards.ChancePack(shuffle_it=False)

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
        self.assertEqual(test_player.cards, [])

        # Find the Get Out Of Jail Card in a pack of Chance cards.
        test_chance = cards.ChancePack(shuffle_it=False)
        test_card = None
        for c in test_chance.pack:
            if c.category == 'Keep Card':
                test_card = c
                break

        test_player.add_card(test_card)
        self.assertEqual(len(test_player.cards), 1)     # Player should now have 1 card.

        # Take the card away from the player.
        removed_card = test_player.remove_card()
        self.assertEqual(len(test_player.cards), 0)     # Player should now have no cards.
        self.assertEqual(removed_card, test_card)       # Removed card should be same as added card.


class TestGame(unittest.TestCase):

    def test_game(self):

        test_game = game.Game(num_players=4, verbose=False)

        # The stats lists should have same number of elements as there are square on the board.
        self.assertEqual(len(test_game.land_on_frequency), len(test_game.board.squares))
        self.assertEqual(len(test_game.turn_end_frequency), len(test_game.board.squares))

        # There should be 4 player objects in the players list.
        self.assertEqual(len(test_game.players), 4)

        # Pick one of the players to continue testing with.
        test_player = test_game.players[0]

        # Check player is currently on Go square.
        # There are 2 different ways to test this. We'll use the 2nd method for rest of the tests.
        self.assertEqual(test_game.board.index_to_square_name(test_player.square), 'Go')
        self.assertEqual(test_game.player_square_name(test_player), 'Go')

        # Check that advance to Pall Mall from Go works OK. This does not involve going past Go.
        passed_go = test_game.advance_to_square(test_player, 'Pall Mall')
        self.assertEqual(test_game.player_square_name(test_player), 'Pall Mall')
        self.assertEqual(passed_go, False)

        # Advance from Pall Mall to Water Works. Again this does not involve going past Go.
        passed_go = test_game.advance_to_square(test_player, 'Water Works')
        self.assertEqual(test_game.player_square_name(test_player), 'Water Works')
        self.assertEqual(passed_go, False)

        # Advance from Water Works to Old Kent Road. This DOES involve going past Go.
        passed_go = test_game.advance_to_square(test_player, 'Old Kent Road')
        self.assertEqual(test_game.player_square_name(test_player), 'Old Kent Road')
        self.assertEqual(passed_go, True)

    def test_jail(self):
        test_game = game.Game(num_players=1, verbose=False)
        test_player = test_game.players[0]

        # Send the test player to Jail.
        test_game.go_to_jail(test_player)
        self.assertEqual(test_game.player_square_name(test_player), 'Jail')
        self.assertEqual(test_player.in_jail, True)
        self.assertEqual(test_player.double_attempts_left, 3)

        # Do try_to_leave_jail max of 3 times, they should always be out by then.
        # In case they got a lucky triple on first attempt, do this test many times.
        for t in range(1000):
            test_game.go_to_jail(test_player)                   # Put the player back in Jail.
            for i in range(3):                                  # Try to leave (up to) 3 times.
                test_game.try_to_leave_jail(test_player)
                if not test_player.in_jail:                     # If let of jail, leave the loop early.
                    break

            # If he's still in Jail after 3 attempts, then next attempt will let him out.
            if test_player.in_jail:
                test_game.try_to_leave_jail(test_player)

            self.assertEqual(test_player.in_jail, False)

        # TODO Unit tests - Check that someone with a Get Out Jail card leave Jail on first attempt.

if __name__ == '__main__':
    unittest.main()
