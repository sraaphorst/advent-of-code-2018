#!/usr/bin/env python3
# day03.py
# By Sebastian Raaphorst, 2018.


import aocd
import re


class FabricCut:
    matcher = re.compile("#(?P<id>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)")

    def __init__(self, string_representation):
        """
        Parse a FabricCut from the string representation used to store it, which is the same one returned by repr.
        :param string_representation: the string representation

        >>> fc = FabricCut('#1 @ 2,3: 4x5')
        >>> (fc.id, fc.left, fc.top, fc.width, fc.height)
        (1, 2, 3, 4, 5)

        >>> fc = FabricCut('abcde')
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        ValueError: Invalid FabricCut representation: "abcde"
        """
        result = FabricCut.matcher.match(string_representation)
        if result is None:
            raise ValueError('Invalid FabricCut representation: "{}"'.format(string_representation))

        self.id = int(result.group("id"))
        self.left = int(result.group("left"))
        self.top = int(result.group("top"))
        self.width = int(result.group("width"))
        self.height = int(result.group("height"))

    def intersects(self, other):
        """
        Simply determine if two FabricCuts intersect.
        :param other: the other FabricCut
        :return: True if the cuts intersect, and False otherwise

        >>> fc1 = FabricCut("#1 @ 1,3: 4x4")
        >>> fc2 = FabricCut("#2 @ 3,1: 4x4")
        >>> fc3 = FabricCut("#3 @ 5,5: 2x2")
        >>> fc1.intersects(fc2) and fc2.intersects(fc1)
        True
        >>> fc1.intersects(fc3) and fc3.intersects(fc1)
        False
        >>> fc2.intersects(fc3) and fc3.intersects(fc2)
        False
        """
        left1, left2 = (self, other) if self.left < other.left else (other, self)
        top1, top2 = (self, other) if self.top < other.top else (other, self)
        return left2.left < left1.left + left1.width and top2.top < top1.top + top1.height

    def intersection(self, other):
        """
        Check if two FabricCuts intersect and provide the size of their intersection in square inches.
        :param other: the other FabricCut
        :return: the number of square inches of their intersection

        >>> fc1 = FabricCut("#1 @ 1,3: 4x4")
        >>> fc2 = FabricCut("#2 @ 3,1: 4x4")
        >>> fc3 = FabricCut("#3 @ 5,5: 2x2")
        >>> fc1.intersection(fc2) == {(3, 3), (3, 4), (4, 3), (4, 4)}
        True
        >>> fc2.intersection(fc1) == {(3, 3), (3, 4), (4, 3), (4, 4)}
        True
        >>> fc1.intersection(fc3)
        set()
        >>> fc3.intersection(fc1)
        set()
        >>> fc2.intersection(fc3)
        set()
        >>> fc3.intersection(fc2)
        set()
        """
        # Check if they can intersect both horizontall and vertically.
        # This is done by checking which of the two is furthest to the left / top, and it the other one's starting
        # position falls within its range.
        left1, left2 = (self, other) if self.left < other.left else (other, self)
        top1, top2 = (self, other) if self.top < other.top else (other, self)

        horizontal_overlap = range(left2.left, min(left2.left + left2.width, left1.left + left1.width))
        vertical_overlap = range(top2.top, min(top2.top + top2.height, top1.top + top1.height))
        intersectons = {(x, y) for x in horizontal_overlap for y in vertical_overlap}
        return intersectons

    def __eq__(self, other):
        """
        Determine if two FabricCuts are equal, which means all their parameters are equal.
        :param other: the other FabricCut
        :return: True if equal, False otherwise

        >>> string_representation = '#1 @ 2,3: 4x5'
        >>> fc1 = FabricCut(string_representation)
        >>> fc2 = FabricCut(string_representation)
        >>> fc3 = FabricCut("#2 @ 3,4: 5x6")
        >>> fc1 == fc2 and fc2 == fc1
        True
        >>> fc1 == fc3 or fc3 == fc1
        False
        """
        return (self.id, self.left, self.top, self.width, self.height) ==\
               (other.id, other.left, other.top, other.width, other.height)

    def __repr__(self):
        """
        Return a representation of a FabricCut that can be made back into a FabricCut.
        :return: the string representation

        >>> string_representation = '#1 @ 2,3: 4x5'
        >>> fc = FabricCut(string_representation)
        >>> string_representation == repr(fc)
        True
        >>> FabricCut(repr(fc)) == fc
        True
        """
        return "#{} @ {},{}: {}x{}".format(self.id, self.left, self.top, self.width, self.height)

    def __str__(self):
        """
        Return the simple string representation of the FabricCut, which is just its id.
        :return: the id as a string

        >>> fc = FabricCut('#1 @ 2,3: 4x5')
        >>> str(fc)
        '1'
        """
        return str(self.id)


def total_intersection_size(fabric_cuts):
    """
    Determine the total size of the intersection of a list of fabric cuts.
    :param fabric_cuts: the list of fabric cuts
    :return: the total size of the intersection

    >>> fabric_cuts = [FabricCut('#1 @ 1,3: 4x4'), FabricCut('#2 @ 3,1: 4x4'), FabricCut('#3 @ 5,5: 2x2'), FabricCut('#4 @ 3,4: 2x2')]
    >>> total_intersection_size(fabric_cuts)
    6
    """
    s = set()
    for i in range(len(fabric_cuts) - 1):
        for j in range(i+1, len(fabric_cuts)):
            s.update(fabric_cuts[i].intersection(fabric_cuts[j]))
    return len(s)


def find_nonintersecting_regions(fabric_cuts):
    """
    Find the one set - if it exists - in fabric_cuts that does not intersect any other.
    :param fabric_cuts: the list of fabric cuts
    :return:
    """
    for i in range(len(fabric_cuts)):
        if {fabric_cuts[i].intersects(fabric_cuts[j]) for j in range(len(fabric_cuts)) if i != j} == {False}:
            return fabric_cuts[i].id
    return None


if __name__ == '__main__':
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=3)
    fabric_cuts = list(map(FabricCut, data.split('\n')))

    a1 = total_intersection_size(fabric_cuts)
    print("a1 = %r" % a1)
    aocd.submit1(a1, year=2018, day=3, session=session, reopen=False)

    a2 = find_nonintersecting_regions(fabric_cuts)
    print("a2 = %r" % a2)
    aocd.submit2(a2, year=2018, day=3, session=session, reopen=False)
