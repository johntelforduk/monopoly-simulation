# Histogram of how many attempts people need to leave jail.

import game

frequencies = [0] * 5

test_game = game.Game(num_players=1, verbose=False)
test_player = test_game.players[0]

for i in range(1000):
    attempts = 0

    test_game.go_to_jail(test_player)               # Send the player to Jail.

    while test_player.in_jail:
        test_game.try_to_leave_jail(test_player)
        attempts += 1

    assert attempts <= 4

    frequencies[attempts] = frequencies[attempts] + 1

print(frequencies)
