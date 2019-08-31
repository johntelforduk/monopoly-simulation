# Monopoly player.

import cards                            # Needed to provide type information for one of the methods.

class Player:

    def __init__(self, player_num: int):

        self.player_num = player_num    # Player number, eg. 1, 2, 3, 4, etc.
        self.money = 1500               # Starting amount of money is £1500.
        self.square = 0                 # Players start the game on square zero, which is Go.
        self.in_jail = False            # Players start the same out of jail.
        self.double_attempts_left = 0   # When player is in Jail, number of attempts at double to escape left.
        self.deeds = []                 # No deeds for player yet.
        self.cards = []                 # No Chance or Community Chest cards yet.
        self.money_at_end_of_turn =[]

        # TODO add list of desired_properties.

        # TODO add risk_appetite.

    def add_card(self, this_card):
        """Add parm card to player's cards."""
        assert (this_card.category == 'Keep Card')                      # Should be a keep-able card.
        self.cards.append(this_card)

    def remove_card(self) -> cards.Card:
        """Remove card from the player's cards."""
        assert (len(self.cards) > 0)                                    # Must be at least one card held by the player.
        this_card = self.cards.pop(0)
        return this_card
