# The game board.


# Superclass for squares on the board.
class Square:

    def __init__(self, name, category, colour):
        self.name = name
        self.category = category
        self.colour = colour

        assert (self.category in {'Go', 'Property', 'Community Chest', 'Tax', 'Station', 'Chance', 'Jail',
                                  'Utility', 'Free Parking', 'Go To Jail'})

        assert (self.colour in {'White', 'Brown', 'Light Blue', 'Pink', 'Orange', 'Red',
                                'Yellow', 'Green', 'Dark Blue'})


# Child class for squares that car capable of being owned by players...
# ... for example Kings Cross Station and Electric Company.
class OwnableSquare(Square):

    def __init__(self, name, category, colour, cost, mortgage):
        Square.__init__(self, name, category, colour)

        # Additional attributes that an ownable square has.
        self.cost = cost                                # Cost of the square.
        self.mortgage = mortgage                        # Mortgage value of the square.
        self.owner = None                               # When square first created on board, it has no owner.
        self.mortgaged = False                          # Is the square currently mortgaged?

    # TODO Write classes for assigning ownership of square to a player, etc.


# Child class for the actual properties in the game, for example Old Kent Road and Mayfair.
class Property(OwnableSquare):

    def __init__(self, name, colour, cost, mortgage, house_price,
                 site_rent, one_house_rent, two_houses_rent, three_houses_rent, four_houses_rent, hotel_rent):
        OwnableSquare.__init__(self, name, 'Property', colour, cost, mortgage)

        # Additional attributes that a property square has.
        self.house_price = house_price

        # List of rents [site, 1 house, 2 houses, 3 houses, 4 houses, hotel]
        self.rent = [site_rent, one_house_rent, two_houses_rent, three_houses_rent, four_houses_rent, hotel_rent]


class Board:

    def __init__(self):
        self.squares = []                           # Each element will be an object specific to the type of square.

        line_no = 1

        with open('squares.csv') as fileobj:
            for line in fileobj:
                if line_no != 1:                    # First line of CSV is a header, so skip it.
                    parsed_line = line.split(',')

                    square_category = parsed_line[1]

                    # If this row from the CSV file is for a property, then add a Property object to the list.
                    if square_category == 'Property':
                        self.squares.append(Property(parsed_line[0],            # Name.
                                                     parsed_line[2],            # Colour.
                                                     int(parsed_line[3]),       # Cost.
                                                     int(parsed_line[4]),       # Mortgage.
                                                     int(parsed_line[5]),       # House Price.
                                                     int(parsed_line[6]),       # Site Rent.
                                                     int(parsed_line[7]),       # One House Rent.
                                                     int(parsed_line[8]),       # Two House Rent.
                                                     int(parsed_line[9]),       # Three House Rent.
                                                     int(parsed_line[10]),      # Four House Rent.
                                                     int(parsed_line[11])       # Hotel Rent.
                                                     ))

                    # Otherwise, add a generic Square object to the list.
                    else:
                        self.squares.append(Square(parsed_line[0],              # Name.
                                                   square_category,             # Category.
                                                   parsed_line[2]))             # Colour.

                line_no += 1

        fileobj.close()                                                         # Finished with the file, so close it.

    def print_square(self, square_number):
        this_square = self.squares[square_number]
        print('Square Number=', square_number,
              '  Name =', this_square.name,
              '  Colour =', this_square.colour, end='')

        if this_square.category == 'Property':
            print('  Cost =', this_square.cost,
                  '  Mortgage =', this_square.mortgage,
                  '  Owner =', this_square.owner,
                  '  Mortgaged =', this_square.mortgaged)
        else:
            print()                         # Carriage return, to start a new line.

    # Print out the whole board.
    def print_board(self):
        for i in range(len(self.squares)):
            self.print_square(i)

    def forwards(self, current, spaces):
        return (current + spaces) % len(self.squares)

    # TODO Come up with a calculated way of moving backwards.
    def backwards(self, current, spaces):
        for i in range(spaces):
            current -= 1
            if current < 0:
                current = len(self.squares) - 1
        return current
