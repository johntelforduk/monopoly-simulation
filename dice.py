# The pair of dice needed for Monopoly.

import random


class TwoDice:

    def __init__(self):
        self.this_throw = 0                 # Total value of this throw of the dice.
        self.is_a_double = False            # True iff the two thrown dice match.

    def roll_one_die(self) -> int:
        """Roll a single die."""
        return random.randint(1, 6)

    def roll_two_dice(self) -> int:
        """Roll a pair of dice."""
        first_die = self.roll_one_die()
        second_die = self.roll_one_die()

        self.this_throw = first_die + second_die
        self.is_a_double = (first_die == second_die)
        return self.this_throw

    def print_dice(self):
        if self.is_a_double:
            print('Dice throw =', self.this_throw, '(a double)')
        else:
            print('Dice throw =', self.this_throw)
