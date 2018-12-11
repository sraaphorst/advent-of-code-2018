#!/usr/bin/env python3
# day_11.py
# By Sebastian Raaphorst, 2018.


import aocd


class SummedAreaTable:
    """
    Given a table, create a summed-area table for that table.
    A summed-area table is a table where entry (x,y) contains the sum of table[i][j] for 0 <= i <= x and 0 <= j <= y.
    This allows us to calculate the sum of elements in any rectangle of the original table with only at most four array
    lookups, i.e. O(1).
    """
    def __init__(self, table):
        """
        Given a table, make a summed-area table for it and wrap it in a class for simplifying computation.
        :param table: the input table
        """
        self.rows = len(table)
        self.cols = len(table[0])

        # Create the summed-area table.
        sa_table = [[0] * 300 for _ in range(300)]
        sa_table[0][0] = table[0][0]

        # In order to not have to deal with avoiding negative values, calculate the first row and column explicitly.
        for i in range(1, 300):
            sa_table[i][0] = table[i][0] + sa_table[i - 1][0]
            sa_table[0][i] = table[0][i] + sa_table[0][i - 1]

        # Now the rest is trivially easy. Proceed over columns and then rows.
        for row in range(1, self.rows):
            for col in range(1, self.cols):
                sa_table[row][col] = table[row][col] + sa_table[row][col - 1] + sa_table[row - 1][col]\
                        - sa_table[row - 1][col - 1]

        self._table = sa_table

    def sum_of(self, x, y, width, height):
        """
        Given a position (x,y) that represents the top left point, find the sum of the elements from the original table
        in a rectangle of the specified width and height.

        :param x: x coordinate of the top-left point
        :param y: y coordinate of the top-left point
        :param width: width of the rectangle of summation
        :param height: height of the rectangle of summation
        :return: the sum of all the elements of the original table in the specified rectangle.
        """
        if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
            raise ValueError('Illegal table coordinates: ({},{})'.format(x, y))
        if height <= 0 or width <= 0:
            raise ValueError('Width and height must both be positive')
        if x + height > self.rows or y + width > self.cols:
            raise ValueError('Rectangle coordinates fall outside of table: ({},{})'.format(x + height, y + width))

        # Calculate the area. If in the first row or column, just return the value to avoid corner cases with
        # negative array indices.
        if x == 0:
            return self._table[0][y + width - 1] - self._table[0][y]
        if y == 0:
            return self._table[x + height - 1][0] - self._table[x][0]

        # Otherwise, this is a normal case.
        return self._table[x-1][y-1] + self._table[x + height - 1][y + width - 1] - self._table[x-1][y + width - 1] \
            - self._table[x + height - 1][y-1]


def calculate_cell_power_level(x, y, serial):
    """
    Calculate the convoluted power level of a cell based on the formula provided.
    :param x: the x coordinate
    :param y: the y coordinate
    :param serial: the serial number of the device
    :return: the power level

    >>> calculate_cell_power_level(3, 5, 8)
    4
    >>> calculate_cell_power_level(122, 79, 57)
    -5
    >>> calculate_cell_power_level(217, 196, 39)
    0
    >>> calculate_cell_power_level(101, 153, 71)
    4
    """
    rack_id = x + 10
    num = (rack_id * y + serial) * rack_id
    if abs(num) < 100:
        # There is no digit in the 100s position, so take it to be zero, and subtract five from it.
        return -5
    else:
        # Fetch the digit in the 100s position and subtract five from it.
        return int(str(num)[-3]) - 5


def create_power_level_table(serial, width=300, height=300):
    """
    Create the width x height power level matrix that is generated by serial.
    :param serial: program input
    :param width: the width of the table
    :param height: the height of the table
    :return: A width x height array of power levels
    """
    return [[calculate_cell_power_level(x, y, serial) for y in range(width)] for x in range(height)]


def find_highest_powered_square(sa_table, n=3):
    """
    Given a serial number, find the n x n square with the highest power level.
    :param sa_table: the summed-area table
    :param n: the dimensions of the square
    :return: the upper left coordinates of the n x n square with maximum power

    >>> find_highest_powered_square(SummedAreaTable(create_power_level_table(18)))
    (29, (33, 45))
    >>> find_highest_powered_square(SummedAreaTable(create_power_level_table(42)))
    (30, (21, 61))
    """
    return max([(sa_table.sum_of(x, y, n, n), (x, y))
                for x in range(sa_table.rows - n + 1)
                for y in range(sa_table.cols - n + 1)])


def find_highest_powered_of_all_squares(sa_table):
    """
    Find the highest power level of all squares.
    :param sa_table: the summed-area table
    :return: the upper left coordinates and size of each cell
    >>> find_highest_powered_of_all_squares(SummedAreaTable(create_power_level_table(18)))
    ((113, (90, 269)), 16)
    """
    return max([(find_highest_powered_square(sa_table, i), i) for i in range(1, 301)])


if __name__ == '__main__':
    day = 11
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)
    serial_data = int(data)
    satable = SummedAreaTable(create_power_level_table(serial_data))

    a1 = '{},{}'.format(*find_highest_powered_square(satable)[1])
    print('a1 = {}'.format(a1))
    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2result = find_highest_powered_of_all_squares(satable)
    a2 = '{},{},{}'.format(a2result[0][1][0], a2result[0][1][1], a2result[1])
    print('a2 = {}'.format(a2))
    aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
