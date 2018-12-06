#!/usr/bin/env python3
# day_6.py
# By Sebastian Raaphorst, 2018.


import aocd


def bounding_box_pt(coords):
    """
    Given a set of coordinatesof points, find the bounding box.
    Then calculate, in this bounding box, for each cell, the point at the minimum Manhattan distance from the
    point. If two or more points are at the same minimum Manhattan distance from the point, then it is set to -1/

    Finally, count the number of cells per point. We are only interested in finite areas, so if a point falls on the
    boundary of the bounding box, it is infinite and we set its area to -1.
    :param coords: the coordinates of the points
    :return: the index of the point with the largest finite area

    # This shows how to consider the last element, we need to add one to the point count.
    # We demonstrate this through the explicit case and then a couple of shuffles.
    >>> bounding_box_pt([(1, 1), (6, 1), (3, 8), (4, 3), (5, 5), (9, 8)])
    17
    >>> bounding_box_pt([(1, 1), (6, 1), (3, 8), (4, 3), (9, 8), (5, 5)])
    17
    >>> A = [(1, 1), (6, 1), (3, 8), (4, 3), (9, 8), (5, 5)]
    >>> from random import shuffle
    >>> shuffle(A)
    >>> bounding_box_pt(A)
    17
    >>> shuffle(A)
    >>> bounding_box_pt(A)
    17
    """
    # The number of points, and split the coordinates into x-values and y-values.
    # Find the largest delta in x coordinates in x-values and y-values, which we use as the dimensions of the
    # bounding box.
    numps = len(coords)
    xs, ys = list(zip(*coords))
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    # Adjust the coordinates so that they fall within the bounding box.
    coords_adj = [(x - xmin, y - ymin) for (x, y) in coords]

    # Set up an array (x, y) for all points in the bounding box, holding a pair (p, d) such that:
    # - p indicates the index of the point closest to adjusted position (x, y); and
    # - d indicates the distance via the Manhattan metric from point p to adjusted position (x, y).
    # If two points are minimally equidistant to (x, y), then we set its p to -1, indicating that it is
    # out of play.
    # minpts[x][y] holds pair (p, d) representing the minimum distance seen so far, as point p having distance d.
    minpts = [[(0, xmax + ymax + 2)] * (ymax - ymin + 1) for _ in range(xmax - xmin + 1)]

    # Iterate over all the adjusted coordinates, find their distances to the (x, y) positions, and determine if
    # this is better, or minimally equidistant, in which case, we set the point to -1.
    for (p, c) in zip(range(len(coords_adj)+1), coords_adj):

        # p is the point index, and c are the adjusted coordinates.
        cx, cy = c

        # Iterate over all the points in the bounding box and check to see if we should modify minpts by the above
        # stated rules.
        for (x,y) in [(x, y) for x in range(xmax - xmin + 1) for y in range(ymax - ymin + 1)]:
            # The Manhattan distance from p to (x, y).
            dist = abs(cx - x) + abs(cy - y)

            # Minimally equidistant: set the point idx to -1.
            if dist == minpts[x][y][1]:
                minpts[x][y] = (-1, dist)
            elif dist < minpts[x][y][1]:
                minpts[x][y] = (p, dist)

    # We are no longer interested in distances, so drop the distance parameter and keep only the point.
    pts = [[e[0] for e in L1] for L1 in minpts]

    # Count the number of cells "won" by each point.
    # If a point lands on the outer border, it falls in an infinite area and is not a viable candidate.
    # It seems like we need the + 1 here to consider the last point for its area.
    # See the example above in bounding_box_pt doctests.
    pcounts = [0] * (numps + 1)
    for (x, y) in [(x, y) for x in range(xmax - xmin + 1) for y in range(ymax - ymin + 1)]:
        p = pts[x][y]
        if x == 0 or y == 0 or x == xmax - xmin or y == ymax - ymin:
            pcounts[p] = -1
        elif pcounts[p] >= 0:
            pcounts[p] += 1

    # Now find the index of the point occurring in the maximum finite area.
    maxdist = max(pcounts)

    # If the max dist is -1, then no point wins. All are infinitely large.
    if maxdist == -1:
        return None
    else:
        return maxdist


if __name__ == '__main__':
    day = 6
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)
    coords = [tuple(map(int, x.split(', '))) for x in data.split('\n')]

    a1 = bounding_box_pt(coords)
    print("a1 = %r" % a1)
    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = None
    print("a2 = %r" % a2)
    #aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
