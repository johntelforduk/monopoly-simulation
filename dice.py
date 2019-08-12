# The pair of dice needed for Monopoly.

import random


class TwoDice:

    def __init__(self):

        self.this_throw = 0                 # Total value of this throw of the dice.
        self.is_a_double = False            # True iff the two thrown dice match.

    # Roll a single die.
    def roll_one_die(self):
        return random.randint(1, 6)

    # Roll a pair of dice.
    def roll_two_dice(self):
        first_die = self.roll_one_die()
        second_die = self.roll_one_die()

        self.this_throw = first_die + second_die
        self.is_a_double = (first_die == second_die)
        return self.this_throw

    def print_dice(self):
        print('Dice throw =', self.this_throw)
