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
        # So turn_end_count[0] is number of times a turn has ended on Go, etc.
        self.land_on_count = [0] * len(self.board.squares)
        self.turn_end_count = [0] * len(self.board.squares)

    def player_square(self, this_player: player.Player) -> board.Square:
        """Return the square that the parm player is currently on."""
        return self.board.index_to_square(this_player.square)

    def player_square_name(self, this_player: player.Player) -> str:
        """Return the name of the square that the parm player is currently on."""
        return self.player_square(this_player).name

    def print_player_status(self, this_player: player.Player):
        """Print a line of status info about the player to stdout."""
        print('Square =', self.player_square_name(this_player), end='')
        if this_player.in_jail:
            print(' (in jail).')
        else:
            print()

    def player_put_on_square(self, this_player: player.Player):
        """When a player lands on a new square, update stats and (possibly) print some status to stdout."""

        # Add to stats about squares landed on.
        self.land_on_count[this_player.square] += 1

        if self.verbose:
            self.print_player_status(this_player)

    # TODO Add method - check_buildable_properties

    # TODO Add method - calc_current_rent

    def take_a_turn(self, this_player: player.Player):
        """Player takes a turn. May involve several throw of dice (due to doubles),
           taking actions due to square landed on (Go To Jail, Chance, etc.), or just trying to leave Jail."""

        if self.verbose:
            print('\nNew turn.  ', end='')
            self.print_player_status(this_player)

        turn_continues = True                       # Set this to False when the turn is over.
        doubles_in_turn = 0                          # Needed so that we send the player to Jail if 3 throws in turn.

        while turn_continues:
            this_throw = 0                              # Zero indicates dice hasn't been thrown yet.

            # Check if player is in jail, and trying getting out of jail if they are.
            if this_player.in_jail:
                this_trow = self.try_to_leave_jail(this_player)
                if this_player.in_jail:
                    turn_continues = False
                if this_trow != 0:                      # Only way to get out of jail is to throw a double.
                    doubles_in_turn += 1

            # If they are still in Jail, then the turn is over.
            if not this_player.in_jail:

                # Now it is time to throw the dice and move...
                # ... but if dice were thrown in Prison, then no need to throw them again.
                if this_throw == 0:
                    self.dice.roll_two_dice()
                    if self.dice.is_a_double:           # Check for a double.
                        doubles_in_turn += 1
                    if self.verbose:
                        self.dice.print_dice()

                # At this point, we know the player is not currently in Jail, and the dice have been thrown,
                # (either in Jail or out of Jail).
                # Since dice have been thrown, it is possible that the limit of 3 doubles in a turn has been met,
                # which sends the player to Jail and ends the turn.
                if doubles_in_turn >= 3:
                    self.go_to_jail(this_player)
                    turn_continues = False

                # At last, we can move the player forward according to the latest dice throw.
                else:
                    this_player.square = self.board.forwards(current=this_player.square, spaces=self.dice.this_throw)
                    self.player_put_on_square(this_player)      # Update stats, print player status.

                    # Take action depending on the type of square they've landed on.
                    self.landed_on_a_square(this_player)

                    # Player may have been put in Jail. If so, the turn is over.
                    if this_player.in_jail:
                        turn_continues = False

            # Only way for turn to continue is if the throw was a double.
            if not (turn_continues and self.dice.is_a_double):
                turn_continues = False

        # Add to stats about squares that turns end on.
        self.turn_end_count[this_player.square] += 1

        if self.verbose:
            print('Turn over.')

    # TODO Add method - player_passed_go
    #  It will increase the player's money by £200 (or £100 if they currently have loan from bank).

    def advance_to_square(self, this_player: player.Player, target_square: str) -> bool:
        """Move the parm player directly to the parm square.
           Return a bool to indicate if the player has passed Go in the process."""
        curr_square = this_player.square

        # Move the player to the target square.
        this_player.square = self.board.find_square(target_square)
        self.player_put_on_square(this_player)                  # Update stats, print player status.

        new_square = this_player.square

        # TODO If the player passed Go due to this move, make call to player_passed_go()

        # If the square that the player has advanced to has a lower index than the one he started on,
        # then he must he passed Go during this move.
        return new_square < curr_square

    def go_to_jail(self, this_player: player.Player):
        """Send the parameter player to Jail."""
        assert not this_player.in_jail      # Only a player who is not in Jail can be sent to Jail.

        if self.verbose:
            print('Sent to Jail!!!')

        self.advance_to_square(this_player, 'Jail')
        this_player.in_jail = True
        this_player.double_attempts_left = 3

    def try_to_leave_jail(self, this_player: player.Player) -> int:
        """Parm is a player who is attempting to get out of Jail.
           Each call to this method is one attempt to leave.
           Return value is any roll of the dice that they did in Jail."""

        assert this_player.in_jail              # Only a player in Jail should try to leave it.

        # Use the player's Get Out Of Jail card, if they have one.
        if len(this_player.cards) > 0:
            removed_card = this_player.remove_card()
            assert (removed_card.card_name[0:21] == 'Get out of jail free.')

            # Put the card back in its home pack.
            assert(removed_card.pack_name in {'Chance', 'Community Chest'})
            if removed_card.pack_name == 'Chance':
                self.chance.add_card(removed_card)
            else:
                self.community_chest.add_card(removed_card)

            # Let the player out of Jail.
            this_player.in_jail = False

            if self.verbose:
                print('Used a Get Of Jail Free Card to leave Jail.')
            return 0

        # Let the player out if he has made three attempts already.
        if this_player.double_attempts_left == 0:
            this_player.in_jail = False
            # TODO If the player fails to roll doubles for three turns, he or she must pay the $50 fine and then
            #  moves the number shown on the dice or skip one turn.

            if self.verbose:
                print('Let out of Jail because they have made 3 attempts at doubles already.')

            return 0

        # Throw dice for a double.
        else:
            self.dice.roll_two_dice()
            if self.verbose:
                print('Attempting to get out of jail with a dice roll. ', end='')
                self.dice.print_dice()

            this_player.double_attempts_left -= 1
            if self.dice.is_a_double:
                this_player.in_jail = False

                if self.verbose:
                    print('Got out of Jail with a dice roll.')

            return self.dice.this_throw

    def landed_on_a_square(self, this_player: player.Player):
        """Do whatever actions the square that the player has landed on demands.
           Recursive, since some actions tell the player to move to another square, which then needs to be acted on."""

        this_square = self.player_square(this_player)
        if this_square.name == 'Go To Jail':
            self.go_to_jail(this_player)

        elif this_square.category in {'Chance', 'Community Chest'}:

            # Make a note of the index of the square that the player was on before action card was acted on.
            square_before_action = this_player.square

            self.land_on_action_square(this_player, this_square)

            # Action card has put the player on a new square. So now do that action.
            if square_before_action != this_player.square:
                self.landed_on_a_square(this_player)

        # TODO Need to add actions for Tax squares, Go, Properties, Stations and Utilities.

    def land_on_action_square(self, this_player: player.Player, this_square: board.Square):
        """Player has landed on either Chance or Community Chest.
           This method does the things that these action squares demand."""

        # Only players who are currently on Chance or Community Chest should do this method.
        assert (self.player_square(this_player).category in {'Chance', 'Community Chest'})

        # Get an action_card from the top of either Chance or Community Chest packs.
        pack_name = this_square.category
        if pack_name == 'Chance':
            action_card = self.chance.take_card()
        else:
            action_card = self.community_chest.take_card()

        if self.verbose:
            action_card.print_card(print_pack=True)

        if action_card.category == 'Keep Card':                 # If it is a keep card, then the player should take it.
            this_player.add_card(action_card)
        elif action_card.category == 'Jail':                    # If Go To Jail, send the player to Jail.
            self.go_to_jail(this_player)
        elif action_card.category == 'Advance':                 # If Advance, send the player to the named square.
            self.advance_to_square(this_player, action_card.advance_to)
        elif action_card.card_name == 'Go back three spaces':   # Move player back 3 squares.
            this_player.square = self.board.backwards(current=this_player.square, spaces=3)
            self.player_put_on_square(this_player)  # Update stats, print player status.
        elif action_card.card_name == 'Go back to Old Kent Road':   # Send player to Old Kent Road.
            this_player.square = self.board.find_square('Old Kent Road')
            self.player_put_on_square(this_player)  # Update stats, print player status.

        # Except for keep cards, put the card back into its pack.
        if action_card.category != 'Keep Card':
            if pack_name == 'Chance':
                self.chance.add_card(action_card)
            else:
                self.community_chest.add_card(action_card)
