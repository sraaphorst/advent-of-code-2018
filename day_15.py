#!/usr/bin/env python3
# day_15.py
# By Sebastian Raaphorst, 2018.


import aocd
from enum import Enum
from copy import deepcopy
import sys


class Terrain(Enum):
    WALL = 1
    FLOOR = 2


class Race(Enum):
    ELF = 1
    GOBLIN = 2


class Critter:
    id = 0

    def __init__(self, race, x, y):
        self.attack_power = 3
        self.hit_points = 200
        self.race = race
        self.x = x
        self.y = y
        self.id = Critter.id
        Critter.id += 1

    def __str__(self):
        return '{}(id={}, x={}, y={}, hp={})'.format('G' if self.race == Race.GOBLIN else 'E', self.id,
                                                     self.x, self.y, self.hit_points)


class Game:
    def __init__(self, data):
        """
        Read the dame setup from the provided data, and we create the immutable data that will be used to play.
        :param data: the block of text passed in as input
        """
        # Maintain a dictionary of (x,y) to critter to simplify sorting reading order.
        self._critters = {}
        self._board = []

        for row, line in enumerate(data.split('\n')):
            new_row = []
            for col, entry in enumerate(list(line)):
                # Process the terrain.
                if entry == '.' or entry == 'E' or entry == 'G':
                    new_row.append(Terrain.FLOOR)
                else:
                    new_row.append(Terrain.WALL)

                # If there is a critter here, add it to the list.
                if entry == 'E':
                    self._critters[(row, col)] = Critter(Race.ELF, row, col)
                elif entry == 'G':
                    self._critters[(row, col)] = Critter(Race.GOBLIN, row, col)
            self._board.append(new_row)

    def print_board(self, critters):
        # Print the playing board and the critters.
        print('rows={}, cols={}'.format(len(self._board), len(self._board[0])))
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if (row, col) in critters:
                    sys.stdout.write('E' if critters[(row, col)].race == Race.ELF else 'G')
                else:
                    sys.stdout.write('#' if self._board[row][col] == Terrain.WALL else '.')
            sys.stdout.write('\n')
        sys.stdout.write('\n')
        for c in critters.values():
            print(c)
        sys.stdout.write('\n\n')

    def play(self):
        """
        Simulate the game, making a copy of the objects so at the leave the base confirguration immutable.
        :return: the sum of the hit points of the survivors multiplied by the number of rounds

        >>> Game(open('day_15_1.dat').read()).play()
        27828
        >>> Game(open('day_15_2.dat').read()).play()
        27730
        >>> Game(open('day_15_3.dat').read()).play()
        36334
        >>> Game(open('day_15_4.dat').read()).play()
        39514
        >>> Game(open('day_15_5.dat').read()).play()
        27755
        >>> Game(open('day_15_6.dat').read()).play()
        28944
        >>> Game(open('day_15_7.dat').read()).play()
        18740
        """
        # Make copies of the data that should be mutable so that we can manipulate it.
        # This comprises the critter dictionary.
        critters = deepcopy(self._critters)

        def can_be_occupied(x, y):
            """
            Determine if position (x, y) can be occupied, (x, y) is in bounds and a floor tile.
            """
            return 0 <= x <= len(self._board) and 0 <= y <= len(self._board[0]) and self._board[x][y] == Terrain.FLOOR

        def list_or_none(L):
            return None if len(L) == 0 else L[0]

        # print("Initial:")
        # self.print_board(critters)

        # Now play the game until all of the critters on one side are dead.
        num_rounds = 0
        while True:
            # We sort the critters to indicate the reading order, i.e. the order in which they act.
            # We sort on the critters keys, i.e. (x, y), but store by ID so we can skip over dead critters.
            critter_order = [critters[(x, y)].id for x, y in sorted(critters)]

            # Now, for each non-dead critter, we must find the shortest path to its nearest enemy, if one exists.
            all_units_acted = True
            for critter_id in critter_order:
                # If the critter was killed, we skip.
                critter = list_or_none([c for c in critters.values() if c.id == critter_id])
                if critter is None:
                    continue

                # We stop combat when some unit cannot act.
                if len([c for c in critters.values() if c.race != critter.race]) == 0:
                    all_units_acted = False
                    break

                # Clear out the enemy to attack:
                enemy_to_attack = None

                # To do this, keep track of visited tiles. Start with the current critter's tile as a path of
                # length 0 and then expand outward. Stop expanding a path when it is adjacent to a critter of the
                # opposite race type.
                covered_tiles = {(critter.x, critter.y)}
                possible_paths = [[(critter.x, critter.y)]]

                while len(possible_paths) > 0:
                    # Check if there are any enemies in a possible path. If so, stop.
                    adjacent_enemies = [(critters[path[-1]], path) for path in possible_paths if path[-1] in critters
                                        and critters[path[-1]].race != critter.race]

                    # If there is an enemy, move towards it (if possible, i.e. not adjacent to it already).
                    if len(adjacent_enemies) > 0:
                        # Pick the weakest enemy to attack, otherwise selecting in reading order,
                        enemy_to_attack, path = sorted(adjacent_enemies,
                                                       key=lambda c: (c[0].hit_points, c[0].x, c[0].y))[0]

                        # In order to move, the path must have length at least three:
                        # The first entry is the present location of the critter;
                        # The second position is an empty position to which it moves; and
                        # The last position is an enemy.
                        if len(path) >= 3:
                            critters[path[1]] = critter
                            oldx, oldy = critter.x, critter.y
                            del critters[(oldx, oldy)]
                            critter.x, critter.y = path[1]

                        # Now we have either moved, or were adjacent to an enemy.
                        break

                    # Otherwise, try all the paths adjacent to the existing paths that can be extended.
                    # We don't use a list comprehension for this as the logic is quite complex.
                    new_possible_paths = []
                    for path in possible_paths:
                        for delta in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                            # Form the new point with which to extend the path.
                            newx, newy = path[-1][0] + delta[0], path[-1][1] + delta[1]

                            # We cannot move to it if:
                            # 1. It has been marked as used; or
                            # 2. It is cannot be occupied (i.e. it out of bounds or not floor); or
                            # 3. An ally occupies it.
                            if (newx, newy) in covered_tiles or not can_be_occupied(newx, newy) or \
                                    ((newx, newy) in critters and critters[(newx, newy)].race == critter.race):
                                covered_tiles.add((newx, newy))
                                continue

                            # Otherwise, extend the path.
                            covered_tiles.add((newx, newy))
                            new_possible_paths.append(path + [(newx, newy)])

                    possible_paths = sorted(new_possible_paths)

                # If we have a marked enemy to attack, attack it.
                if enemy_to_attack is not None and \
                        abs(critter.x - enemy_to_attack.x) + abs(critter.y - enemy_to_attack.y) == 1:
                    # print("Enemy {} is attacking enemy {}".format(critter, enemy_to_attack))
                    # Hurt the enemy.
                    enemy_to_attack.hit_points -= critter.attack_power
                    if enemy_to_attack.hit_points <= 0:
                        # print("Dead: {}".format(enemy_to_attack))
                        del critters[(enemy_to_attack.x, enemy_to_attack.y)]

            if all_units_acted:
                num_rounds += 1
            else:
                break

            # print("*** AFTER ROUND {} ***".format(num_rounds))
            # self.print_board(critters)

        # print(num_rounds, sum([c.hit_points for c in critters.values()]))
        # self.print_board(critters)
        # At this point, sum up the remaining HP of all critters (since one race will be dead), and multiply by the
        # number of rounds.
        return num_rounds * sum([c.hit_points for c in critters.values()])


if __name__ == '__main__':
    day = 15
    session = aocd.get_cookie()

    data = open('day_15_3.dat').read()
    g = Game(data)
    a = g.play()
    print(a)
#    data = aocd.get_data(session=session, year=2018, day=day)

    a1 = None
    print('a1 = %r' % a1)
#    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = None
    print('a2 = %r' % a2)
#    aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
