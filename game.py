# Game class for Monopoly simulation.

import dice
import board
import cards
import player


class Game:

    def __init__(self, num_players: int, verbose: bool):

        self.num_players = num_players
        self.verbose = verbose                  # True means a lot of trace will be sent to stdout.

        # Make a list of players.
        self.players = []                       # Each element is a player object.
        for i in range(num_players):
            self.players.append(player.Player())

        self.board = board.Board()              # The game needs a board...
        self.dice = dice.TwoDice()              # ...and some dice.

        # Create the card packs.
        self.chance = cards.ChancePack(shuffle_it=True)
        self.community_chest = cards.CommunityChestPack(shuffle_it=True)

        # These attributes are for collecting stats as the game is played.
        # Initialised to a list of zeros, one for each square on the board.
        # So turn_end_frequency[0] is number of times a turn has ended on Go, etc.
        self.land_on_frequency = [0] * len(self.board.squares)
        self.turn_end_frequency = [0] * len(self.board.squares)

    def player_square(self, this_player: player.Player) -> board.Square:
        """Return the square that the parm player is currently on."""
        return self.board.index_to_square(this_player.square)

    def player_square_name(self, this_player: player.Player) -> str:
        """Return the name of the square that the parm player is currently on."""
        return self.player_square(this_player).name

    def print_player_status(self, this_player: player.Player):
        print('Square =', self.player_square_name(this_player))

    # TODO Add method - check_buildable_properties

    # TODO Add method - calc_current_rent

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
        this_player.square = self.board.forwards(current=this_player.square, spaces=self.dice.this_throw)

        # Add to stats about squares landed on.
        self.land_on_frequency[this_player.square] += 1

        if self.verbose:
            self.print_player_status(this_player)

        # TODO Act depending on the type of square they've landed on.

    # TODO Update turn_end_frequency.

    def advance_to_square(self, this_player: player.Player, target_square: str) -> bool:
        """Move the parm player directly to the parm square.
           Return a bool to indicate if the player has passed Go in the process."""
        curr_square = this_player.square

        # Move the player to the target square.
        this_player.square = self.board.find_square(target_square)

        new_square = this_player.square

        # If the square that the player has advanced to has a lower index than the one he started on,
        # then he must he passed Go during this move.
        return new_square < curr_square

    def go_to_jail(self, this_player: player.Player):
        """Send the parameter player to Jail."""
        self.advance_to_square(this_player, 'Jail')
        this_player.in_jail = True
        this_player.double_attempts_left = 3

    def try_to_leave_jail(self, this_player: player.Player) -> int:
        """Parm is a player who is attempting to get out of Jail.
           Each call to this method is one attempt to leave.
           Return value is any roll of the dice that they did in Jail."""

        assert this_player.in_jail              # Only a player in Jail should try to leave it.
        # TODO Use the player's Get Out Of Jail card, if they have one.

        # Let the player out if he has made three attempts already.
        if this_player.double_attempts_left == 0:
            this_player.in_jail = False
            # TODO If the player fails to roll doubles for three turns, he or she must pay the $50 fine and then
            #  moves the number shown on the dice or skip one turn.
            return 0

        # Throw dice for a double.
        else:
            self.dice.roll_two_dice()
            this_player.double_attempts_left -= 1
            if self.dice.is_a_double:
                this_player.in_jail = False
            return self.dice.this_throw
