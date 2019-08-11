# Monopoly player.


class Player:

    def __init__(self):

        self.money = 1500
        self.square = 0                 # Players start the game on square zero, which is Go.
        self.in_jail = False            # Players start the same out of jail.
        self.turns_in_jail = 0
        self.deeds = []                 # No deeds for player yet.
        self.cards = []                 # No Chance or Community Chest cards yet.

        # TODO add list of desired_properties.

        # TODO add risk_appetite.
