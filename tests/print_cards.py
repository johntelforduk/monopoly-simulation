# Print out the Chance & Community Cards packs.

import cards

chance_cards = cards.ChancePack(shuffle_it=True)
chance_cards.print_pack()

print()

community_chest_cards = cards.CommunityChestPack(shuffle_it=True)
community_chest_cards.print_pack()
