# Game class for Monopoly simulation.

import dice
import board
import cards
import player


class Game:

    def __init__(self, num_players):

        self.num_players = num_players
        self.players = []

        # Add player
        for i in range(num_players):
            self.players.append(player.Player())

        self.board = board.Board()
        self.dice = dice.TwoDice()

        self.chance = cards.CardPack('Chance', 'chance_cards.csv')
        self.community_chest = cards.CardPack('Community Chest', 'community_chest_cards.csv')

    # TODO check_buildable_properties

    # TODO calc_current_rent
