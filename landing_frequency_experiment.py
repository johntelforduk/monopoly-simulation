import matplotlib.pyplot as pyplot
import numpy as np
import game


# Convert the parm list of numbers to a list of percentages of the sum of the list.
# For example list_to_percentages([0.5, 0.5, ,2,3,4]) returns [5, 5, 20, 30, 40].
def list_to_percentages(this_list):
    percentage = lambda x: 100 * x / sum(this_list)
    return list(map(percentage, this_list))


test_game = game.Game(1, verbose=False)

# Throw dice and move player piece some number of times.
for i in range(1000):
    test_game.throw_dice_and_move(test_game.players[0])

# print(test_game.land_on_frequency)

land_on_percent = list_to_percentages(test_game.land_on_frequency)  # Work out frequency percentages.

# Make a label list of square names for the graph.
label = []
for i in test_game.board.squares:
    label.append(i.name)

index = np.arange(len(label))

fig, ax = pyplot.subplots(nrows=1, ncols=1, figsize=(8, 5))
pyplot.bar(index, land_on_percent)
# pyplot.xlabel('Genre', fontsize=5)
pyplot.ylabel('Frequency', fontsize=10)
pyplot.xticks(index, label, fontsize=8, rotation=90)
pyplot.title('Land On Frequency')
pyplot.tight_layout()                       # Ensure that the property names fit on the plot area.
pyplot.show()
