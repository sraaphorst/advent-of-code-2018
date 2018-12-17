#!/usr/bin/env python3
# day_13.py
# By Sebastian Raaphorst, 2018.


import aocd
from enum import Enum


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class Track(Enum):
    NORTH_SOUTH = 1
    EAST_WEST = 2
    SLASH = 3  # /
    BACKSLASH = 4  # \
    INTERSECTION = 5
    EMPTY = 6


class Cart:
    id = 0

    def __init__(self, xpos: int, ypos: int, dir: Direction):
        self.id = Cart.id
        Cart.id += 1
        self.x = xpos
        self.y = ypos
        self._dir = dir
        self._intersection_state = 0
        self.collision_state = False

    def tick(self, rails, carts, remove_crashes=False):
        # If the cart has already collided, there is nothing to do.
        if self.collision_state:
            return None

        oldx, oldy = self.x, self.y

        if rails[(self.x, self.y)] == Track.NORTH_SOUTH:
            if self._dir == Direction.NORTH:
                self.x -= 1
            elif self._dir == Direction.SOUTH:
                self.x += 1
            else:
                raise ValueError("Cart {} heading in illegal direction when encountered north-south".format(self.id))
        elif rails[(self.x, self.y)] == Track.EAST_WEST:
            if self._dir == Direction.EAST:
                self.y += 1
            elif self._dir == Direction.WEST:
                self.y -= 1
            else:
                raise ValueError("Cart {} heading in illegal direction when encountered east-west".format(self.id))
        elif rails[(self.x, self.y)] == Track.SLASH:
            if self._dir == Direction.NORTH:
                self.y += 1
                self._dir = Direction.EAST
            elif self._dir == Direction.EAST:
                self.x -= 1
                self._dir = Direction.NORTH
            elif self._dir == Direction.SOUTH:
                self.y -= 1
                self._dir = Direction.WEST
            elif self._dir == Direction.WEST:
                self.x += 1
                self._dir = Direction.SOUTH
        elif rails[(self.x, self.y)] == Track.BACKSLASH:
            if self._dir == Direction.NORTH:
                self.y -= 1
                self._dir = Direction.WEST
            elif self._dir == Direction.EAST:
                self.x += 1
                self._dir = Direction.SOUTH
            elif self._dir == Direction.SOUTH:
                self.y += 1
                self._dir = Direction.EAST
            elif self._dir == Direction.WEST:
                self.x -= 1
                self._dir = Direction.NORTH
        elif rails[(self.x, self.y)] == Track.INTERSECTION:
            if self._intersection_state == 0:
                if self._dir == Direction.NORTH:
                    self.y -= 1
                    self._dir = Direction.WEST
                elif self._dir == Direction.EAST:
                    self.x -= 1
                    self._dir = Direction.NORTH
                elif self._dir == Direction.SOUTH:
                    self.y += 1
                    self._dir = Direction.EAST
                elif self._dir == Direction.WEST:
                    self.x += 1
                    self._dir = Direction.SOUTH
            elif self._intersection_state == 1:
                if self._dir == Direction.NORTH:
                    self.x -= 1
                elif self._dir == Direction.EAST:
                    self.y += 1
                elif self._dir == Direction.SOUTH:
                    self.x += 1
                elif self._dir == Direction.WEST:
                    self.y -= 1
            elif self._intersection_state == 2:
                if self._dir == Direction.NORTH:
                    self.y += 1
                    self._dir = Direction.EAST
                elif self._dir == Direction.EAST:
                    self.x += 1
                    self._dir = Direction.SOUTH
                elif self._dir == Direction.SOUTH:
                    self.y -= 1
                    self._dir = Direction.WEST
                elif self._dir == Direction.WEST:
                    self.x -= 1
                    self._dir = Direction.NORTH
            self._intersection_state = (self._intersection_state + 1) % 3

        # Update carts and check for collision.
        del carts[(oldx, oldy)]
        if (self.x, self.y) in carts:
            self.collision_state = True
            carts[(self.x, self.y)].collistion_state = True

            if remove_crashes:
                del carts[(self.x, self.y)]

            # The output expects (y, x)
            return self.y, self.x
        else:
            carts[(self.x, self.y)] = self
            return None


class Rails:
    def __init__(self, rails, carts):
        self._rails = rails
        self._carts = carts

    def tick(self, remove_crashes=False):
        # Sort the carts by their x, y coordinates:
        cart_order = sorted(self._carts.keys())
        for x, y in cart_order:
            if (x, y) in self._carts:
                result = self._carts[(x, y)].tick(self._rails, self._carts, remove_crashes)
                if result is not None and not remove_crashes:
                    return result
        return None

    def run_simulation(self):
        """
        Run the simulation, finding the first collision.
        :return: the x, y coordinates of the first collision

        >>> data = open('day_13_1.dat').read()
        >>> r = process_rails(data)
        >>> r.run_simulation()
        (7, 3)
        """
        result = None
        while result is None:
            result = self.tick()
        return result

    def run_cart_removal_simulation(self):
        """
        Run the simulation, in which crashed carts are removed, and find the position of the last standing cart.
        :return: the (y, x) coordinate of the last standing cart

        >>> data = open('day_13_2.dat').read()
        >>> r = process_rails(data)
        >>> r.run_cart_removal_simulation()
        (6, 4)
        """
        while len(self._carts) > 1:
            self.tick(True)
        assert(len(self._carts) == 1)
        for cart in self._carts.values():
            return cart.y, cart.x


def process_rails(data):
    rails = {}
    carts = {}

    # Process the rails first.
    for x, line in enumerate(data.split('\n')):
        for y, symbol in enumerate(line):
            # Process rails
            if symbol == ' ':
                rails[(x, y)] = Track.EMPTY
            elif symbol == '|' or symbol == '^' or symbol == 'v':
                rails[(x, y)] = Track.NORTH_SOUTH
            elif symbol == '-' or symbol == '>' or symbol == '<':
                rails[(x, y)] = Track.EAST_WEST
            elif symbol == '/':
                rails[(x, y)] = Track.SLASH
            elif symbol == '\\':
                rails[(x, y)] = Track.BACKSLASH
            elif symbol == '+':
                rails[(x, y)] = Track.INTERSECTION
            else:
                raise ValueError('Illegal input symbol at ({},{}): {}'.format(x, y, symbol))

    # Process the carts.
    for x, line in enumerate(data.split('\n')):
        for y, symbol in enumerate(line):
            if symbol == '^':
                carts[(x, y)] = Cart(x, y, Direction.NORTH)
            elif symbol == '>':
                carts[(x, y)] = Cart(x, y, Direction.EAST)
            elif symbol == 'v':
                carts[(x, y)] = Cart(x, y, Direction.SOUTH)
            elif symbol == '<':
                carts[(x, y)] = Cart(x, y, Direction.WEST)

    return Rails(rails, carts)


if __name__ == '__main__':
    day = 13
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)

    r1 = process_rails(data)
    a1 = r1.run_simulation()
    print('a1 = {}'.format(a1))
    aocd.submit1('{},{}'.format(a1[0], a1[1]), year=2018, day=day, session=session, reopen=False)

    r2 = process_rails(data)
    a2 = r2.run_cart_removal_simulation()
    print('a2 = {}'.format(a2))
    aocd.submit2('{},{}'.format(a2[0], a2[1]), year=2018, day=day, session=session, reopen=False)
