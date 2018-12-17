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

    def __init__(self, xpos: int, ypos: int, dir: Direction, cart_state):
        self.id = Cart.id
        Cart.id += 1
        self._x = xpos
        self._y = ypos
        self._dir = dir
        self._cart_state = cart_state.copy()
        self.collision_state = False

    def tick(self, rails, carts):
        # If the cart has already collided, there is nothing to do.
        if self.collision_state:
            return None

        oldx, oldy = self._x, self._y

        if rails[(self._x, self._y)] == Track.NORTH_SOUTH:
            if self._dir == Direction.NORTH:
                self._x -= 1
            elif self._dir == Direction.SOUTH:
                self._x += 1
            else:
                raise ValueError("Cart {} heading in illegal direction when encountered north-south".format(self.id))
        elif rails[(self._x, self._y)] == Track.EAST_WEST:
            if self._dir == Direction.EAST:
                self._y += 1
            elif self._dir == Direction.WEST:
                self._y -= 1
            else:
                raise ValueError("Cart {} heading in illegal direction when encountered east-west".format(self.id))
        elif rails[(self._x, self._y)] == Track.SLASH:
            if self._dir == Direction.NORTH:
                self._y += 1
                self._dir = Direction.EAST
            elif self._dir == Direction.EAST:
                self._x -= 1
                self._dir = Direction.NORTH
            elif self._dir == Direction.SOUTH:
                self._y -= 1
                self._dir = Direction.WEST
            elif self._dir == Direction.SOUTH:
                self._x += 1
                self._dir = Direction.SOUTH
        elif rails[(self._x, self._y)] == Track.BACKSLASH:
            if self._dir == Direction.NORTH:
                self._y -= 1
                self._dir = Direction.WEST
            elif self._dir == Direction.EAST:
                self._x += 1
                self._dir = Direction.SOUTH
            elif self._dir == Direction.SOUTH:
                self._y += 1
                self._dir = Direction.EAST
            elif self._dir == Direction.SOUTH:
                self._x -= 1
                self._dir = Direction.NORTH
        elif rails[(self._x, self._y)] == Track.INTERSECTION:
            if self._cart_state[(self._x, self._y)] == 0:
                if self._dir == Direction.NORTH:
                    self._y -= 1
                    self._dir = Direction.WEST
                elif self._dir == Direction.EAST:
                    self._x -= 1
                    self._dir = Direction.NORTH
                elif self._dir == Direction.SOUTH:
                    self._y += 1
                    self._dir = Direction.EAST
                elif self._dir == Direction.WEST:
                    self._x += 1
                    self._dir = Direction.SOUTH
            elif self._cart_state[(self._x, self._y)] == 1:
                if self._dir == Direction.NORTH:
                    self._x -= 1
                elif self._dir == Direction.EAST:
                    self._y += 1
                elif self._dir == Direction.SOUTH:
                    self._x += 1
                elif self._dir == Direction.WEST:
                    self._y -= 1
            elif self._cart_state[(self._x, self._y)] == 2:
                if self._dir == Direction.NORTH:
                    self._y += 1
                    self._dir = Direction.EAST
                elif self._dir == Direction.EAST:
                    self._x += 1
                    self._dir = Direction.SOUTH
                elif self._dir == Direction.SOUTH:
                    self._y -= 1
                    self._dir = Direction.WEST
                elif self._dir == Direction.WEST:
                    self._x -= 1
                    self._dir = Direction.NORTH
            self._cart_state[(oldx, oldy)] = (self._cart_state[(oldx, oldy)] + 1) % 3

        # Update carts and check for collision.
        del carts[(oldx, oldy)]
        if (self._x, self._y) in carts:
            self.collision_state = True
            carts[(self._x, self._y)].collistion_state = True
            return self._x, self._y
        else:
            carts[(self._x, self._y)] = self
            return None


class Rails:
    def __init__(self, rails, carts):
        self._rails = rails
        self._carts = carts

    def tick(self):
        # Sort the carts by their x, y coordinates:
        cart_order = sorted(self._carts.keys())
        for x, y in cart_order:
            result = self._carts[(x, y)].tick(self._rails, self._carts)
            if result is not None:
                return result
        return None

    def run_simulation(self):
        """
        Run the simulation, finding the first collision.
        :return: the x, y coordinates of the first collision

        >>> data = open('day_13.dat').read()
        >>> r = process_rails(data)
        >>> r.run_simulation()
        (7, 3)
        """
        result = None
        while result is None:
            result = self.tick()
        return result


def process_rails(lines):
    rails = {}
    carts = {}
    cart_state = {}

    # Process the rails. We do this first to ascertain the cart_state, which contains the intersection data.
    for x, line in enumerate(lines.split('\n')):
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
                cart_state[(x, y)] = 0
            else:
                raise ValueError('Illegal input symbol at ({},{}): {}'.format(x, y, symbol))

    # Process the carts
    for x, line in enumerate(lines.split('\n')):
        for y, symbol in enumerate(line):
            if symbol == '^':
                carts[(x, y)] = Cart(x, y, Direction.NORTH, cart_state)
            elif symbol == '>':
                carts[(x, y)] = Cart(x, y, Direction.EAST, cart_state)
            elif symbol == 'v':
                carts[(x, y)] = Cart(x, y, Direction.SOUTH, cart_state)
            elif symbol == '<':
                carts[(x, y)] = Cart(x, y, Direction.WEST, cart_state)

    return Rails(rails, carts)


if __name__ == '__main__':
    day = 13
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)

    a1 = None
    print('a1 = %r' % a1)
    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = None
    print('a2 = %r' % a2)
    aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
