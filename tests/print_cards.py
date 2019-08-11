# Print out the Chance & Community Cards packs.

import cards


chance_cards = cards.CardPack('Chance', 'chance_cards.csv')
chance_cards.print_pack()
print()
chance_cards.shuffle()
chance_cards.print_pack()
