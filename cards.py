# Chance and Community Chest cards.

import random                               # Needed to shuffle the Chance and Community Chest cards.


class Card:

    def __init__(self, pack_name: str, card_name: str, category: str, money_amount: int, advance_to: str):
        # Chance or Community Chest.
        # Need the pack name on the card, so the we know which pack to return it to after player is finished with it.
        self.pack_name = pack_name

        self.card_name = card_name          # Advance to Bond Street', etc.
        self.category = category            # Money, Advance, Keep Card, Other
        self.money_amount = money_amount    # (+ve for player gains money, -ve for loose money)
        self.advance_to = advance_to        # Name of square to advance to.

        assert(self.pack_name in {'Chance', 'Community Chest'})
        assert(self.category in {'Money', 'Advance', 'Keep Card', 'Other'})

    def print_card(self, print_pack: bool):
        """Print out info about the parm card to stdout."""
        if print_pack:
            print('Pack =', self.pack_name, '  ', end='')

        print('Card =', self.card_name, '  Category =', self.category, end='')

        if self.category == 'Money':
            print('  Money Amount =', self.money_amount)
        elif self.category == 'Advance':
            print('  To =', self.advance_to)
        else:
            print()


# Parent class for packs of cards.
class CardPack:

    def add_card(self, new_card):
        """Add parm card to bottom of pack."""
        self.pack.append(new_card)

    def shuffle(self):
        """Shuffle the pack of cards."""
        random.shuffle(self.pack)

    def __init__(self, pack_name: str, filename: str):

        self.pack_name = pack_name
        self.pack = []                                      # List of card objects currently in the card pack.

        line_no = 1

        with open(filename) as fileobj:
            for line in fileobj:
                if line_no != 1:                            # First line of CSV is a header, so skip it.

                    parsed_line = line.rstrip('\n').split(',')

                    self.add_card(Card(pack_name=pack_name,
                                       card_name=parsed_line[0],
                                       category=parsed_line[1],
                                       money_amount=int(parsed_line[2]),
                                       advance_to=parsed_line[3]))
                line_no += 1

    def print_pack(self):
        print(self.pack_name)
        for p in self.pack:
            p.print_card(print_pack=False)

    def take_card(self):
        """Returns one card from top of pack. Removes the card from pack."""
        return self.pack.pop(0)


# Child class for Chance cards.
# Having this child class means that details like the CSV filename is contained in this module.
class ChancePack(CardPack):

    def __init__(self, shuffle_it: bool):

        CardPack.__init__(self, pack_name='Chance', filename='chance_cards.csv')
        if shuffle_it:
            self.shuffle()


# Child class for Community Chest cards.
class CommunityChestPack(CardPack):

    def __init__(self, shuffle_it: bool):

        CardPack.__init__(self, pack_name='Community Chest', filename='community_chest_cards.csv')
        if shuffle_it:
            self.shuffle()
