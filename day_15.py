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


def list_or_none(L):
    """
    If a list is a singleton, return the element, and otherwise None.
    """
    return None if len(L) == 0 else L[0]


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

    # def __str__(self):
    #     return '{}(id={}, x={}, y={}, attack={}, hp={})'.format('G' if self.race == Race.GOBLIN else 'E', self.id,
    #                                                  self.x, self.y, self.attack_power, self.hit_points)

    def __str__(self):
        return '{}({})'.format('G' if self.race == Race.GOBLIN else 'E', self.hit_points)


class Game:
    delta = [(0, -1), (-1, 0), (1, 0), (0, 1)]

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
        for row in range(len(self._board)):
            baddies = []
            for col in range(len(self._board[row])):
                if (row, col) in critters:
                    sys.stdout.write('E' if critters[(row, col)].race == Race.ELF else 'G')
                else:
                    sys.stdout.write('#' if self._board[row][col] == Terrain.WALL else '.')
                    baddies = sorted([c for c in critters.values() if c.x == row], key=lambda c: c.y)
            sys.stdout.write('  ' + ', '.join([str(c) for c in baddies]))
            sys.stdout.write('\n')
        sys.stdout.write('\n')

    def play(self, critters=None, debug=False):
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
        >>> Game(open('day_15_8.dat').read()).play()[0]
        18468
        >>> Game(open('day_15_9.dat').read()).play()[0]
        10234
        """
        # Make copies of the data that should be mutable so that we can manipulate it.
        # This comprises the critter dictionary.
        critters = deepcopy(self._critters) if critters is None else deepcopy(critters)

        def can_be_occupied(tile):
            """
            Determine if position (x, y) can be occupied, (x, y) is in bounds and a floor tile.
            """
            x, y = tile
            return 0 <= x <= len(self._board) and \
                   0 <= y <= len(self._board[0]) and \
                   self._board[x][y] == Terrain.FLOOR and \
                   (x, y) not in critters

        if debug:
            print("Initial:")
            self.print_board(critters)

        def adjacent_enemies(tile, race):
            """
            Return the positions of enemies to the specified race that are adjacent to tile (x,y).
            """
            adj = []
            for dx, dy in Game.delta:
                newx, newy = tile[0] + dx, tile[1] + dy
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
                adj_enemies = sorted(adjacent_enemies((critter.x, critter.y), critter.race),
                                     key=lambda x: critters[x].hit_points)
                if len(adj_enemies) > 0:
                    # print("Critter {} will attack".format(critter))
                    enemy_to_attack = critters[adj_enemies[0]]

                # Case 2:
                else:
                    # BFS.
                    moves = [(critter.x + dx, critter.y + dy) for dx, dy in Game.delta]
                    moves = [m for m in moves if can_be_occupied(m)]

                    # Maintain a list of the best moves.
                    best_moves = []

                    # Now iterate over the moves, as this is how we would start off in reading order from our location.
                    for move in moves:
                        mx, my = move

                        # If this puts us adjacent to an enemy, then stop.
                        if len(adjacent_enemies(move, critter.race)) > 0:
                            best_moves.append((move, 1, move))

                        # Maintain a dictionary of the shortest way we've found to get to a tile.
                        covered_tiles = {m: 1 for m in moves}
                        covered_tiles[(critter.x, critter.y)] = 0

                        # Maintain a stack of the most distant tiles to process for the BFS.
                        stack = [(mx + dx, my + dy) for (dx, dy) in Game.delta]
                        stack = [s for s in stack if s not in covered_tiles and can_be_occupied(s)]

                        distance = 1
                        cont = True
                        while cont:
                            distance += 1
                            new_stack = []

                            # Look for new tiles to add.
                            for tile in stack:
                                if tile in covered_tiles:
                                    continue
                                covered_tiles[tile] = distance

                                tx, ty = tile
                                # If there is an enemy adjacent to the tile, it's the best we can do.
                                if len(adjacent_enemies(tile, critter.race)):
                                    best_moves.append((move, distance, tile))
                                    cont = False
                                    continue

                                # Add the newly reachable tiles.
                                new_tiles = [(tx + dx, ty + dy) for (dx, dy) in Game.delta]
                                new_stack += [t for t in new_tiles if t not in covered_tiles and can_be_occupied(t)]

                            stack = list(set(new_stack))
                            if not stack:
                                cont = False

                    # Filter out the moves that we can use.
                    best_move = None
                    if best_moves:
                        # First condition: distance.
                        min_dist = min(b[1] for b in best_moves)
                        best_moves = [b for b in best_moves if b[1] == min_dist]

                        # Second condition: for distance ties, choose first destination tile in reading order.
                        best_moves.sort(key=lambda x: x[2])
                        best_moves = [b for b in best_moves if b[2] == best_moves[0][2]]

                        # Third condition: for ties on both, take the first step in reading order.
                        best_moves.sort(key=lambda x: x[0])
                        best_moves = [b for b in best_moves if b[0] == best_moves[0][0]]

                        best_move = best_moves[0][0]

                        # Move.
                        critters[best_move] = critter
                        del critters[(critter.x, critter.y)]
                        critter.x, critter.y = best_move

                        # If we are not adjacent to an enemy, attack the weakest one.
                        adj_enemies = sorted(adjacent_enemies((critter.x, critter.y), critter.race),
                                             key=lambda x: critters[x].hit_points)
                        if len(adj_enemies) > 0:
                            # print("Critter {} will attack".format(critter))
                            enemy_to_attack = critters[adj_enemies[0]]

                if enemy_to_attack is not None:
                    # print("{} is attacking {}".format(critter, enemy_to_attack))
                    enemy_to_attack.hit_points -= critter.attack_power
                    if enemy_to_attack.hit_points <= 0:
                        del critters[(enemy_to_attack.x, enemy_to_attack.y)]

            if all_units_acted:
                num_rounds += 1
            else:
                break

            if debug:
                print("*** AFTER ROUND {} ***".format(num_rounds))
                self.print_board(critters)

        # At this point, sum up the remaining HP of all critters (since one race will be dead), and multiply by the
        # number of rounds.
        if debug:
            print("*** AFTER ROUND {} ***".format(num_rounds))
            self.print_board(critters)
        num_elves = len([c for c in critters.values() if c.race == Race.ELF])
        # print("{} * {}".format(num_rounds, sum([c.hit_points for c in critters.values()])))
        return num_rounds * sum([c.hit_points for c in critters.values()]), num_elves

    def determine_elf_strength(self, debug=False):
        """
        Run simulations with ever-increasing strengths for elves until we finally achieve a point where all of the
        elves survive, and beat the goblins.
        :return: Return the score representing this scenario.

        # >>> Game(open('day_15_2.dat').read()).determine_elf_strength()
        # 4988
        >>> Game(open('day_15_4.dat').read()).determine_elf_strength()
        31284
        >>> Game(open('day_15_5.dat').read()).determine_elf_strength()
        3478
        >>> Game(open('day_15_6.dat').read()).determine_elf_strength()
        6474
        >>> Game(open('day_15_7.dat').read()).determine_elf_strength()
        1140
        >>> Game(open('day_15_8.dat').read()).determine_elf_strength()
        120
        >>> Game(open('day_15_9.dat').read()).determine_elf_strength()
        943
        """
        attack_power = 3

        critters = deepcopy(self._critters)
        elves = [c for c in critters.values() if c.race == Race.ELF]

        while True:
            attack_power += 1
            for e in elves:
                e.attack_power = attack_power

            score, pop = self.play(critters, debug)
            # print("str={}, survivors={}/{}".format(attack_power, pop, len(elves)))
            if pop == len(elves):
                return score


if __name__ == '__main__':
    day = 15
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)

    # 190012
    #a1 = Game(data).play()[0]
    #print('a1 = %r' % a1)
    #aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    # 34364
    a2 = Game(data).determine_elf_strength(debug=True)
    print('a2 = %r' % a2)
    #aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
