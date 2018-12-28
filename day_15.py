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

    def play(self, critters=None):
        """
        Simulate the game, making a copy of the objects so at the leave the base confirguration immutable.
        :return: the sum of the hit points of the survivors multiplied by the number of rounds, and the number
                 of elves that survived, if any

        >>> Game(open('day_15_1.dat').read()).play()[0]
        27828
        >>> Game(open('day_15_2.dat').read()).play()[0]
        27730
        >>> Game(open('day_15_3.dat').read()).play()[0]
        36334
        >>> Game(open('day_15_4.dat').read()).play()[0]
        39514
        >>> Game(open('day_15_5.dat').read()).play()[0]
        27755
        >>> Game(open('day_15_6.dat').read()).play()[0]
        28944
        >>> Game(open('day_15_7.dat').read()).play()[0]
        18740
        """
        # Make copies of the data that should be mutable so that we can manipulate it.
        # This comprises the critter dictionary.
        critters = deepcopy(self._critters) if critters is None else deepcopy(critters)

        def can_be_occupied(x, y):
            """
            Determine if position (x, y) can be occupied, (x, y) is in bounds and a floor tile.
            """
            return 0 <= x <= len(self._board) and 0 <= y <= len(self._board[0]) and self._board[x][y] == Terrain.FLOOR

        def list_or_none(L):
            return None if len(L) == 0 else L[0]

        # print("Initial:")
        # self.print_board(critters)

        # Get the critters adjacent to a tile.
        def adjacent_enemies(x, y, race):
            adj = []
            for delta in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                newx, newy = x + delta[0], y + delta[1]
                if (newx, newy) in critters and critters[(newx, newy)].race != race:
                    adj.append((newx, newy))
            return adj

        # Now play the game until all of the critters on one side are dead.
        num_rounds = 0
        while True:
            # We sort the critters to indicate the reading order, i.e. the order in which they act.
            # We sort on the critters keys, i.e. (x, y), but store by ID so we can skip over dead critters.
            critter_order = [critters[(x, y)].id for x, y in sorted(critters)]

            # Now, for each non-dead critter, we must find the shortest path to its nearest enemy, if one exists.
            all_units_acted = True
            for critter_id in critter_order:
                # print("Moving critter {}".format(critter_id))
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

                # We have two cases to consider:
                # 1. If any enemies are adjacent to us, pick the the weakest one.
                # 2. Otherwise, pick the enemy closest to us and move towards them, breaking ties with reading order.
                # If there are immediately adjacent enemies, simply attack the weakest.

                # Case 1:
                adj_enemies = sorted(adjacent_enemies(critter.x, critter.y, critter.race),
                                     key=lambda x: critters[x].hit_points)
                if len(adj_enemies) > 0:
                    # print("Critter {} will attack".format(critter))
                    enemy_to_attack = critters[adj_enemies[0]]

                # Case 2:
                else:
                    # To do this, keep track of visited tiles. Start with the current critter's tile as a path of
                    # length 0 and then expand outward. Stop expanding a path when it is adjacent to a critter of the
                    # opposite race type.
                    covered_tiles = {(critter.x, critter.y)}
                    possible_paths = [[(critter.x, critter.y)]]

                    # Extend the paths, if possible.
                    while len(possible_paths) > 0:
                        new_possible_paths = []
                        for path in possible_paths:
                            for delta in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                                # Form the new point with which to extend the path.
                                newx, newy = path[-1][0] + delta[0], path[-1][1] + delta[1]

                                # We cannot move to it if:
                                # 1. It has been marked as used; or
                                # 2. It cannot be occupied (i.e. it is out of bounds or not floor); or
                                # 3. An ally occupies it.
                                if (newx, newy) in covered_tiles or (not can_be_occupied(newx, newy)) or \
                                        ((newx, newy) in critters and critters[(newx, newy)].race == critter.race):
                                    covered_tiles.add((newx, newy))
                                    continue

                                # Otherwise, extend the path.
                                covered_tiles.add((newx, newy))
                                new_possible_paths.append(path + [(newx, newy)])

                        possible_paths = sorted(new_possible_paths)

                        # Do any of our possible paths take us to an enemy?
                        enemy_paths = [p for p in possible_paths
                                       if len(adjacent_enemies(p[-1][0], p[-1][1], critter.race)) > 0]

                        # If so, pick the reading order path and move one square.
                        if len(enemy_paths) > 0:
                            enemy_path = enemy_paths[0]
                            # print("{} moves on path: {}".format(critter, enemy_path))
                            newx, newy = enemy_path[1]
                            oldx, oldy = critter.x, critter.y
                            del critters[(oldx, oldy)]
                            critters[(newx, newy)] = critter
                            critter.x = newx
                            critter.y = newy

                            # If we are now in range of an enemy, attack the weakest.
                            adj_enemies = sorted(adjacent_enemies(critter.x, critter.y, critter.race),
                                                 key=lambda x: critters[x].hit_points)
                            if len(adj_enemies) > 0:
                                # print("Critter {} will attack".format(critter))
                                enemy_to_attack = critters[adj_enemies[0]]
                            break

                if enemy_to_attack is not None:
                    # print("{} is attacking {}".format(critter, enemy_to_attack))
                    enemy_to_attack.hit_points -= critter.attack_power
                    if enemy_to_attack.hit_points <= 0:
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
        # print("*** AFTER ROUND {} ***".format(num_rounds))
        # self.print_board(critters)
        num_elves = len([c for c in critters.values() if c.race == Race.ELF])
        # print("{} * {}".format(num_rounds, sum([c.hit_points for c in critters.values()])))
        return num_rounds * sum([c.hit_points for c in critters.values()]), num_elves

    def determine_elf_strength(self):
        """
        Run simulations with ever-increasing strengths for elves until we finally achieve a point where all of the
        elves survive, and beat the goblins.
        :return: Return the score representing this scenario.

        >>> Game(open('day_15_2.dat').read()).determine_elf_strength()
        4988
        >>> Game(open('day_15_4.dat').read()).determine_elf_strength()
        31284
        >>> Game(open('day_15_5.dat').read()).determine_elf_strength()
        3478
        >>> Game(open('day_15_6.dat').read()).determine_elf_strength()
        6474
        >>> Game(open('day_15_7.dat').read()).determine_elf_strength()
        1140
        """
        attack_power = 4

        critters = deepcopy(self._critters)
        elves = [c for c in critters.values() if c.race == Race.ELF]

        while True:
            for e in elves:
                e.attack_power = attack_power

            score, pop = self.play(critters)
            # print("str={}, survivors={}/{}".format(attack_power, pop, len(elves)))
            if pop == len(elves):
                return score

            attack_power += 1


if __name__ == '__main__':
    day = 15
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)

    #Game(open('day_15_2.dat').read()).play()
    a1 = Game(data).play()[0]
    print('a1 = %r' % a1)
    #aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = Game(data).determine_elf_strength()
    print('a2 = %r' % a2)
    #aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
