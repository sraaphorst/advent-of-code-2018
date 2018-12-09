#!/usr/bin/env python3
# day_05.py
# By Sebastian Raaphorst, 2018.


import aocd


def flip(c):
    """
    Flip a character's polarity, i.e. a maps to A, B maps to b, etc.
    :param c: the single character
    :return: the reversed character wrt case

    >>> flip('a')
    'A'
    >>> flip('B')
    'b'
    """
    return c.upper() if c.islower() else c.lower()


def simplify_polymer(polymer, ignore = ''):
    """
    Take a string representing a polymer, and keep negating adjacent elements of different polarity until the
    string is in its simplest form.
    :param polymer: the string representing the polymer
    :param ignore: try ignoring this polymer and its companion of inverse polarity
    :return: the simplified polymer

    >>> simplify_polymer('a')
    'a'
    >>> simplify_polymer('aA')
    ''
    >>> simplify_polymer('abBA')
    ''
    >>> simplify_polymer('abAB')
    'abAB'
    >>> simplify_polymer('aabAAB')
    'aabAAB'
    >>> simplify_polymer('dabAcCaCBAcCcaDA')
    'dabCBAcaDA'
    """
    # This is easily done with a stack, which will represent the simplified polymer.
    stack = []
    for p in polymer:
        if p.lower() == ignore or p.upper() == ignore:
            continue
        if len(stack) > 0 and stack[-1] == flip(p):
            stack.pop()
        else:
            stack.append(p)

    return ''.join(stack)


def ignore_troublesome_polymer(polymer):
    """
    See what the possible shortest string is by ignoring one of the polymers and its polymer of inverse polarity.
    :param polymer: the string representing the polymer
    :return: the simplified polymore

    >>> ignore_troublesome_polymer('dabAcCaCBAcCcaDA')
    'daDA'
    """
    s = set(polymer.lower())
    return min([simplify_polymer(polymer, i) for i in s], key=lambda p: len(p))


if __name__ == '__main__':
    day = 5
    session = aocd.get_cookie()
    polymer = aocd.get_data(session=session, year=2018, day=day)

    a1 = len(simplify_polymer(polymer))
    print('a1 = %r' % a1)
    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = len(ignore_troublesome_polymer(polymer))
    print('a2 = %r' % a2)
    aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
