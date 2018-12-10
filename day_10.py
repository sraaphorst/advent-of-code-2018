#!/usr/bin/env python3
# day_D.py
# By Sebastian Raaphorst, 2018.


import aocd
import re


class Point:
    """
    A Point, which consists of an initial position and a velocity.
    """
    def __init__(self, position, velocity):
        self._position = position
        self._velocity = velocity

    def at_time(self, t):
        return self._position[0] + t * self._velocity[0], self._position[1] + t * self._velocity[1]

    def __repr__(self):
        return "Point(p=({},{}), v=({},{}))".format(*(self._position + self._velocity))


def parse_point(line):
    """
    Parse a Point from an input line.
    :param line: the input line
    :return: the parsed Point object

    >>> parse_point('position=<-3, 11> velocity=< 1, -2>')
    Point(p=(-3,11), v=(1,-2))
    """
    # Given a line, parse the position and the velocity.
    match = re.match('position=<\s*(?P<px>-?\d+),\s*(?P<py>-?\d+)>\s*velocity=<\s*(?P<vx>-?\d+)\s*,\s*(?P<vy>-?\d+)>',
                     line)
    if match is None:
        raise ValueError("Illegal line format: %s" % line)

    return Point((int(match['px']), int(match['py'])), (int(match['vx']), int(match['vy'])))


def positions_at_t(points, t):
    """
    Given a list of Points and a time t, find their positions at time t
    :param points: the list of Points
    :param t: the time t
    :return: a list of pairs indicating the position of the points at time t
    """
    return [p.at_time(t) for p in points]


def distance_at_t(points, t):
    """
    Determine the sum of all the distances of the Points at time t using the easy-to-calculate Manhattan metric.
    We could use the Euclidean metric but the extra computation is entirely unnecessary.
    :param points: the list of Points
    :param t: the time t
    :return: the sum of the distances between all pairs of points for time t
    """
    positions_t = positions_at_t(points, t)
    return sum([abs(p0[0] - p1[0]) + abs(p0[1] + p1[1]) for p0 in positions_t for p1 in positions_t])


def draw_message(points):
    # delta_t will be tuned to get t. A beginning value of 1000 for t is simply a guess; as long as we have a
    # positive integer, the solution will emerge, but if too low, it will take a very long time.
    t = 1
    delta_t = 1000

    # We look for the local minimum distance using a gradient descent algorithm.
    while True:
        # dist = distance_at_t(points, t)/len(points)
        dist = distance_at_t(points, t)

        # Sanity check to see if we are decreasing; if not, switch directions and decrease delta_t.
        dist_prev = distance_at_t(points, t-1)
        dist_next = distance_at_t(points, t+1)

        # Change directions?
        if delta_t > 0 and dist_prev < dist:
            delta_t = -int(delta_t / 2)
        elif delta_t < 0 and dist_next < dist:
            delta_t = -int(delta_t / 2)

        # Inefficient way to check if we are at the local minimum.
        if dist_prev >= dist and dist <= dist_next:
            break

        t += delta_t

    # We now have the minimum distance time, t, and we can print the diagram.
    pos = positions_at_t(points, t)
    x_positions, y_positions = list(zip(*pos))
    xmin, xmax = min(x_positions), max(x_positions)
    ymin, ymax = min(y_positions), max(y_positions)
    deltax = xmax - xmin + 1
    deltay = ymax - ymin + 1

    grid = [[' '] * deltax for _ in range(deltay)]
    for p in pos:
        xpos = p[0] - xmin
        ypos = p[1] - ymin
        grid[ypos][xpos] = '#'
    for line in grid:
        print(''.join(line))

    print("Number of seconds is %r" % t)


# This puzzle is unique, because it requires human identification of the letters formed when the points are in their
# proper position, unless one wanted to go crazy and do some character parsing / recognition, which seems unnecessarily
# complicated.
# My answer was ECKXJLJF, which occurred at time 10880.
if __name__ == '__main__':
    day = 10
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)
    data_points = [parse_point(line) for line in data.split('\n')]

    draw_message(data_points)
