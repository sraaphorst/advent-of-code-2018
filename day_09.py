#!/usr/bin/env python3
# day_09.py
# By Sebastian Raaphorst, 2018.


import aocd


class Marble:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = self if left is None else left
        self.right = self if right is None else right


def calculate_highest_score(num_players, upper_marble):
    """
    Simulate the marble game with the following rules:
    1. Marbles 0 through upper_marble inclusive are played in a circle, one by one.
    2. If the marble is a multiple of 23, keep it and add it and the marble 7 spaces counterclockwise to your score.
       Remove that marble. The current marble becomes the one clockwise to that.
    3. Else, place the marble in position between 1 and 2 clockwise of the current marble. Make it the current.
    Use a doubly linked list to make operations constant.

    :param num_players: number of p layers
    :param upper_marble: highest marble number
    :return: the highest player score

    >>> calculate_highest_score(9, 25)
    32
    >>> calculate_highest_score(10, 1618)
    8317
    >>> calculate_highest_score(13, 7999)
    146373
    >>> calculate_highest_score(17, 1104)
    2764
    >>> calculate_highest_score(21, 6111)
    54718
    >>> calculate_highest_score(30, 5807)
    37305
    """

    base = Marble()
    current_marble = base

    scores = [0] * num_players
    current_player = 1

    for new_marble in range(1, upper_marble + 1):
        # if new_marble % 100 == 0:
        #     print("{} / {}".format(new_marble, upper_marble + 1))
        # If multiple of 23, add to score, and look back seven marbles, add to score, and remove.
        if new_marble % 23 == 0:
            for _ in range(7):
                current_marble = current_marble.left
            scores[current_player] += new_marble + current_marble.value

            # Remove current marble and become next marble.
            current_marble.left.right = current_marble.right
            current_marble.right.left = current_marble.left
            current_marble = current_marble.right

        else:
            m = Marble(value=new_marble, left=current_marble.right, right=current_marble.right.right)
            current_marble.right.right.left = m
            current_marble.right.right = m
            current_marble = m

        current_player = (current_player + 1) % num_players

    return max(scores)


if __name__ == '__main__':
    day = 9
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day).split()
    players = int(data[0])
    highest_marble = int(data[6])

    a1 = calculate_highest_score(players, highest_marble)
    print('a1 = %r' % a1)
    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = calculate_highest_score(players, 100 * highest_marble)
    print('a2 = %r' % a2)
    aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
