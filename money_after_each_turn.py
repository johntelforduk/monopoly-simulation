# Work out how much money players have after each turn (1 player, no deed buying or house buying).

import matplotlib.pyplot as pyplot                              # For drawing bar chart.
import numpy as np
from statistics import mean
import sys                                                      # For parsing parms.
import game
import rotate_list
import curried_percentile as cp


print("""Decisions & Assumptions.
1. The program sends one player around the board for a specified number of turns. 
2. There is no buying or selling of properties.
2. Whenever the player goes to Jail, if he holds a Get Out Of Jail card, he will use it to leave Jail immediately.
   Otherwise, he will attempt to throw doubles in order to try to leave Jail.
   After 3 unsuccessful attempts to throw doubles, he will leave Jail on his next turn.""")

assert(len(sys.argv) == 4)                                      # There should be 3 parms passed to this program.
parm_turns = int(sys.argv[1])
parm_games = int(sys.argv[2])
parm_verbose = sys.argv[3] == 'True'

money = []

# Play a lot of games, with a lot of turns per game.
for g in range(parm_games):
    test_game = game.Game(num_players=1, verbose=parm_verbose)

    for t in range(parm_turns):
        test_game.take_a_turn(test_game.players[0])

    money.append(test_game.players[0].money_at_end_of_turn)

money_rotated = rotate_list.rotate(money)

# Calculate stats.
averages = list(map(mean, money_rotated))
low_percentile = list(map(cp.curry_percentile(10), money_rotated))
high_percentile = list(map(cp.curry_percentile(90), money_rotated))

# Make a label list for the x-axis.
label = []
for i in range(parm_turns):
    label.append(str(i + 1))

index = np.arange(len(label))

fig, ax = pyplot.subplots(nrows=1, ncols=1, figsize=(10, 5))
ax.plot(label, averages, color='blue', label='Mean Average')
ax.plot(label, low_percentile, color='red', label='10th Percentile')
ax.plot(label, high_percentile, color='green', label='90th Percentile')
pyplot.legend(loc='upper left')
pyplot.ylabel('Money (£)', fontsize=10)
pyplot.xlabel('Turn', fontsize=10)

pyplot.xticks(index, label, fontsize=8, rotation=90)
pyplot.title('Money At End Of Each Turn (' + '{:,}'.format(parm_games) + ' games)')
pyplot.tight_layout()
pyplot.show()
