# Little function to rotate a list.


def rotate(grid):
    return [[x[i] for x in grid] for i in range(len(grid[0]))]
