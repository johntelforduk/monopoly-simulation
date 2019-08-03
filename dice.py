# The pair of dice needed for Monopoly.

import random


# Function to roll a single die.
def roll_a_die():
    return random.randint(1, 6)

# Class for a pair of dice.
class TwoDice:

    def __init__(self):
        self.this_throw = 0                 # Total value of this throw of the dice.
        self.is_a_double = False            # True iff the two thrown dice match.

    def roll(self):
        first_die = roll_a_die()
        second_die = roll_a_die()

        self.this_throw = first_die + second_die
        self.is_a_double = (first_die == second_die)
        return self.this_throw
