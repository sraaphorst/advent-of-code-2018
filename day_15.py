#!/usr/bin/env python3
# day_15.py
# By Sebastian Raaphorst, 2018.


import aocd
from enum import Enum


class Terrain(Enum):
    WALL = 1
    FLOOR = 2


class Race(Enum):
    ELF = 1
    GOBLIN = 2


class Critter:
    def __init__(self, race, x, y):
        self.attack_power = 3
        self.hit_points = 200
        self.race = race
        self.x = x
        self.y = y


class Game:
    def __init__(self, data):
        self._critters = []
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
                    self._critters.append(Critter(Race.ELF, row, col))
                elif entry == 'G':
                    self._critters.append(Critter(Race.GOBLIN, row, col))

    def play(self):
        # Create a dict of critters to make it easier to do lookups.
        critter_positions = {(c.x, c.y): c for c in self._critters}

        while True:
            # We stop when there is only one type of critter left.
            goblins = {c for c in self._critters if c.race == Race.GOBLIN}
            elves = {c for c in self._critters if c.race == Race.ELF}
            if len(goblins) == 0 or len(elves) == 0:
                break

            # Sort by reading order.
            self._critters.sort(key=lambda c: (c.x, c.y))
            for c in self._critters:
                # Find the shortest path to a foe using basic BFS.
                paths = {(c.x, c.y): []}
                covered = {(c.x, c.y)}

                path = None
                enemy = None
                while len(paths) > 0:
                    # Find if there are any enemy critters in range yet.
                    # Sort by the length of the path, and then break ties by reading order.
                    nearest = sorted([(len(paths[(x, y)]), paths[(x, y)])
                                      for (x, y) in paths.keys()
                                      if (x, y) in critter_positions and c.race != critter_positions[(x, y)].race])
                    if len(nearest) > 0:
                        # We have a critter in range.
                        path = nearest[0][2]
                        enemy = critter_positions[(nearest[1][0], nearest[1][1])]
                        break

                    # Expand our search.
                    new_paths = {}
                    for (px, py) in paths:
                        for (dx, dy) in [(-1,0), (1,0), (0, -1), (0, 1)]:
                            newx = px + dx
                            newy = py + dy

                            # Reject covered ground, walls, and critters that are the same as us.
                            if (newx, newy) in covered:
                                continue
                            if self._board[newx][newy] == Terrain.WALL:
                                continue
                            if (newx, newy) in critter_positions and critter_positions[(newx, newy)].race == c.race:
                                continue

                            # Extend the path.
                            new_paths[(newx, newy)] = paths[(px, py)] + [(newx, newy)]
                            covered.add((newx, newy))
                    paths = new_paths

                # If we have a path, try to move to the first position on it.
                if path is not None and len(path) > 1:
                    del critter_positions[(c.x, c.y)]
                    c.x += path[0][0]
                    c.y += path[0][0]
                    critter_positions[(c.x, c.y)] = c

                # Now if there is an enemy adjacent, attack it.
                if enemy is not None and abs(enemy.x - c.x) + abs(enemy.y - c.y):
                    enemy.hp -= c.attack_power
                    if enemy.hp < 0:
                        if enemy.race == Race.GOBLIN:
                            goblins.remove(enemy)
                        else:
                            elves.remove(enemy)
                        del critter_positions[(enemy.x, enemy.y)]






if __name__ == '__main__':
    day = 15
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)

    a1 = None
    print('a1 = %r' % a1)
    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = None
    print('a2 = %r' % a2)
    aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
