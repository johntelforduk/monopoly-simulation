import matplotlib.pyplot as pyplot
import numpy as np
import game


# Convert the parm list of numbers to a list of percentages of the sum of the list.
# For example list_to_percentages([0.5, 0.5, ,2,3,4]) returns [5, 5, 20, 30, 40].
def list_to_percentages(this_list):
    percentage = lambda x: 100 * x / sum(this_list)
    return list(map(percentage, this_list))


print("""Decisions & Assumptions in this experiment
1. The experiment is one player going round the board for a large number of turns. 
2. There is no buying or selling of properties.
2. Whenever a player goes to Jail, if he holds a Get Out Of Jail card, he will use it to leave Jail immediately.
   Otherwise, he will attempt to throw doubles in order to try to leave Jail. After 3 unsuccessful attempts to throw doubles, he will leave Jail on his next turn.""")

test_game = game.Game(num_players=1, verbose=False)

# Take a number of turns for this player.
for turns in range(1000000):
    test_game.take_a_turn(test_game.players[0])

land_on_percent = list_to_percentages(test_game.land_on_count)  # Work out frequency percentages.
end_on_percent = list_to_percentages(test_game.turn_end_count)  # Work out frequency percentages.

# Make a label list of square names for the graph.
label = []
sq = 0
for i in test_game.board.squares:
    label.append(i.name)
    print("{0:.2f}".format(land_on_percent[sq]), i.name)
    sq += 1

index = np.arange(len(label))
width = 0.27                                # The width of the bars.

fig, ax = pyplot.subplots(nrows=1, ncols=1, figsize=(8, 5))
pyplot.bar(index - width/2, land_on_percent, width=width, align='center', color='b', label='Land On')
pyplot.bar(index + width/2, end_on_percent, width=width, align='center', color='g', label='End Turn On')
pyplot.legend(loc='upper left')
pyplot.ylabel('Frequency (percentage)', fontsize=10)
pyplot.xticks(index, label, fontsize=8, rotation=90)
pyplot.title('Square Frequencies')
pyplot.tight_layout()                       # Ensure that the property names fit on the plot area.
pyplot.show()
