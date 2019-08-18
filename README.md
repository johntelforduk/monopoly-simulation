# Monopoly Simulation
Simulation of the popular property trading game.

#### Roadmap
1. DONE: Player movement mechanics. Board and dice. Chance & Community Chest for cards which move the player. Go To Jail and different ways of leaving jail.
2. DONE: Work out square frequencies. How often do players land on each square, and how often do they end their turn on each square. Graphing of results.
3. TO DO: Financial parts of the game. Deed buying, house building, rent calculation and collection. Chance and Community Chest cards with financial implications.
4. TO DO: Simulate players with different strategies. For example, players with preference for buying certain sets of properties, different appetites for risk taking (how much of their cash they will spend on houses, etc.).

#### Installation
```
pip install matplotlib
```

#### To Watch A Player Going Round The Board
This allows you to check that tha player movement mechanics are working as expected - dice rolling, Chance and Community Chest cards that move players, 'Go to Jail', etc.
```
python one_player_on_board.py 25 True
```
The 1st parameter is how many turns the player will take. `True` for the 2nd parameter tells the program to print info about the player's movements to stdout. Example output [here](https://github.com/johntelforduk/monopoly-simulation/blob/master/docs/example_player_going_round_board.txt).

#### To Calculate Square Frequencies
```
python one_player_on_board.py 1000000 False
```
The 1st parameter is how many turns the player will take. `False` for the 2nd parameter tells the program to not send detailed info about the player's movement to stdout.

![Frequencies after 1M turns](https://github.com/johntelforduk/monopoly-simulation/blob/master/docs/frequencies_after_1M_turns.png)

#### Class Diagram
There is a class diagram [here](https://github.com/johntelforduk/monopoly-simulation/blob/master/docs/monopoly_class_diagram.jpeg).
 
#### Useful Info
Property rents, etc.
http://www.jdawiseman.com/papers/trivia/monopoly-rents.html

House prices,
https://en.wikipedia.org/wiki/List_of_London_Monopoly_locations

UK board layout,
https://en.wikipedia.org/wiki/Template:London_Monopoly_board_layout

Official rules,
https://en.wikibooks.org/wiki/Monopoly/Official_Rules

List of Chance cards,
https://monopolyguide.com/london/monopoly-london-list-of-chance-cards/

List of Community Chest cards,
https://monopolyguide.com/london/monopoly-london-list-of-community-chest-cards/

The Mathematics of Winning Monopoly (Matt Parker & Hannah Fry)
https://youtu.be/ubQXz5RBBtU