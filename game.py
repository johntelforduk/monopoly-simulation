# Game class for Monopoly simulation.

import dice
import board
import cards
import player


class Game:

    def __init__(self, num_players, verbose):

        self.num_players = num_players
        self.verbose = verbose                  # True means a lot of trace will be sent to stdout.
        self.players = []                       # Each element is a player object.

        # Make a list of players.
        for i in range(num_players):
            self.players.append(player.Player())

        self.board = board.Board()              # The game needs a board...
        self.dice = dice.TwoDice()              # ...and some dice.

        # Create the Chance cards, and shuffle them.
        self.chance = cards.CardPack('Chance', 'chance_cards.csv')
        self.chance.shuffle()

        # Create the Community Chest cards, and shuffle them.
        self.community_chest = cards.CardPack('Community Chest', 'community_chest_cards.csv')
        self.community_chest.shuffle()

        # These attributes are for collecting stats as the game is played.
        # Initialised to a list of zeros, one for each square on the board.
        # So turn_end_frequency[0] is number of times a turn has ended on Go, etc.
        self.land_on_frequency = [0] * len(self.board.squares)
        self.turn_end_frequency = [0] * len(self.board.squares)

    # TODO Add method - check_buildable_properties

    # TODO Add method - calc_current_rent

    def print_player_status(self, this_player):
        print('Square =', self.board.squares[this_player.square].name)


    # TODO Method - go_to_jail.

    # TODO Method - land_on_square. If the player is not in jail, do the action(s) required by the square they are on.


    # Player takes a throw_dice_and_move of the game.
    def throw_dice_and_move(self, this_player):

        # TODO Add logic for taking another throw if last one was a double.

        # TODO Add logic for going to jail if 3 doubles in one throw_dice_and_move.

        # TODO Add logic for checking if player is in jail, and trying ways of getting out of jail if they are.

        if self.verbose:
            self.print_player_status(this_player)

        # Begin the throw_dice_and_move by rolling the dice.
        self.dice.roll_two_dice()
        if self.verbose:
            self.dice.print_dice()

        # Move the player's piece forward according to dice roll.
        this_player.square = self.board.forwards(this_player.square, self.dice.this_throw)

        # Add to stats about squares landed on.
        self.land_on_frequency[this_player.square] += 1

        if self.verbose:
            self.print_player_status(this_player)


        # TODO Act depending on the type of square they've landed on.

    # TODO Update turn_end_frequency.
