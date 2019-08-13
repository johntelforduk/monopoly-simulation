# The game board and deed cards.


# Squares on the board.
class Square:

    def __init__(self, name: str, category: str, colour: str, deed):
        self.name = name                                # Old Kent Road, Electric Company, etc.
        self.category = category                        # Go, Chance, Property, etc.
        self.colour = colour                            # Background colour of the square.
        self.deed = deed                                # None means deed has been sold to a player.
        self.who_owns_it = None                         # Useful if deed sold to player.

        assert (self.category in {'Go', 'Property', 'Community Chest', 'Tax', 'Station', 'Chance', 'Jail',
                                  'Utility', 'Free Parking', 'Go To Jail'})

        assert (self.colour in {'White', 'Brown', 'Light Blue', 'Pink', 'Orange', 'Red',
                                'Yellow', 'Green', 'Dark Blue'})


# Superclass for title deed card. Needed for any square that can be owned.
# Includes Properties (Old Kent Road, etc), Utilities and Stations.
class Deed:

    def __init__(self, name: str, cost: int):
        self.name = name                                # For example 'Old Kent Road'.
        self.cost = cost                                # Normal cost of the deed.
        self.mortgage_value = int(cost / 2)             # Rules of game say mortgage is half normal cost of deed.
        self.mortgaged = False                          # Is the square currently mortgaged?
        self.current_rent_rate = 0                      # Will increase as houses are built, sets of stations grow, etc.


# Child class for properties that can have houses built on, for example Old Kent Road and Mayfair.
class PropertyDeed(Deed):

    def __init__(self, name, cost,
                 house_price,
                 site_rent, one_house_rent, two_houses_rent, three_houses_rent, four_houses_rent, hotel_rent):

        Deed.__init__(self, name, cost)

        # Additional attributes that a property square has.
        self.house_price = house_price
        self.currently_buildable = False                # Houses can't be built on it yet - no player has whole set.

        # List of rents [site, 1 house, 2 houses, 3 houses, 4 houses, hotel]
        self.rent = [site_rent, one_house_rent, two_houses_rent, three_houses_rent, four_houses_rent, hotel_rent]

    # TODO Add methods like build_house, demolish_house.


class Board:

    def calc_colour_group_sizes(self):
        for s in self.squares:
            if s.category == 'Property':                    # For property squares only (Old Kent Road, etc.)
                if s.colour in self.colour_group_size:
                    self.colour_group_size[s.colour] += 1   # Colour already in dictionary, so increment count.
                else:
                    self.colour_group_size[s.colour] = 1    # New colour, so add it.

    def __init__(self):
        self.squares = []                           # Each element will be an object specific to the type of square.
        self.colour_group_size = {}                 # Key=Colour, Value=Number of squares with that colour.

        line_no = 1

        with open('squares.csv') as fileobj:
            for line in fileobj:
                if line_no != 1:                    # First line of CSV is a header, so skip it.
                    parsed_line = line.split(',')

                    square_category = parsed_line[1]

                    # If this row from the CSV file is for a property, then add a Property object to the list.
                    if square_category == 'Property':
                        this_deed = PropertyDeed(name=parsed_line[0],
                                                 cost=int(parsed_line[3]),
                                                 house_price=int(parsed_line[5]),
                                                 site_rent=int(parsed_line[6]),
                                                 one_house_rent=int(parsed_line[7]),
                                                 two_houses_rent=int(parsed_line[8]),
                                                 three_houses_rent=int(parsed_line[9]),
                                                 four_houses_rent=int(parsed_line[10]),
                                                 hotel_rent=int(parsed_line[11]))
                    elif square_category in {'Station', 'Utility'}:
                        this_deed = Deed(name=parsed_line[0],
                                         cost=int(parsed_line[3]))
                    else:                                                       # Go, Chance, etc.
                        this_deed = None                                        # This square has no deed.

                    # Add the square to the board, including the deed object.
                    self.squares.append(Square(parsed_line[0],                  # Name.
                                               square_category,                 # Category.
                                               parsed_line[2],                  # Colour.
                                               this_deed))                      # Deed.

                line_no += 1

        fileobj.close()                                                         # Finished with the file, so close it.
        self.calc_colour_group_sizes()

    def print_square(self, square_number: int):
        this_square = self.squares[square_number]
        print('Square Number=', square_number,
              '  Name =', this_square.name,
              '  Colour =', this_square.colour, end='')

        if this_square.deed is not None:
            print('  Cost =', this_square.deed.cost, end='')

            if this_square.category == 'Property':
                print('  House Price =', this_square.deed.house_price, end='')
        print()                         # Carriage return, to start a new line.

    # Print out the whole board.
    def print_board(self):
        for i in range(len(self.squares)):
            self.print_square(i)

    def forwards(self, current: int, spaces: int) -> int:
        return (current + spaces) % len(self.squares)

    # TODO Come up with a calculated way of moving backwards, rather than this iterative approach.
    def backwards(self, current: int, spaces: int) -> int:
        for i in range(spaces):
            current -= 1
            if current < 0:
                current = len(self.squares) - 1
        return current

    def find_square(self, target_name: str) -> int:
        """Return the square index of the parm name. Return None if no such square with that name."""
        found_square_num = None
        for i in range(len(self.squares)):
            if target_name == self.squares[i].name:
                found_square_num = i
                break
        return found_square_num

    def index_to_square(self, this_index: int) -> Square:
        """Return the square with parm index number."""
        return self.squares[this_index]

    def index_to_square_name(self, this_index: int) -> str:
        """Return the name of the square with parm index number."""
        return self.index_to_square(this_index).name
