#!/usr/bin/env python3

import aocd

def frequency(freqs):
    """
    Given a list of frequencies of the form [+-]\d+, with one per line, find their sum.
    :param freqs: the list of frequencies
    :return: the sum of the frequencies

    >>> frequency([+1, -2, +3, +1])
    3
    >>> frequency([+1, +1, +1])
    3
    >>> frequency([+1, +1, -2])
    0
    >>> frequency([-1, -2, -3])
    -6
    """
    return sum(freqs)


def frequency_generator(freqs):
    """
    Given a file of frequencies, i.e. a line-separated list of numbers of the form [+-]\d+, stream
    them infinitely.
    :param freqs: the list of frequencies
    :return: the next frequency
    """
    n = 0
    while True:
        if n == len(freqs):
            n = 0
        yield freqs[n]
        n = n + 1


def find_repeated_frequency(freqs):
    """
    For a list of frequencies that affect the current state, find the first repeating frequency.
    :param freqs: the list of frequencies
    :return: the first repeated frequency

    >>> find_repeated_frequency([+1, -2, +3, +1])
    2
    >>> find_repeated_frequency([+1, -1])
    0
    >>> find_repeated_frequency([+3, +3, +4, -2, -4])
    10
    >>> find_repeated_frequency([-6, +3, +8, +5, -6])
    5
    >>> find_repeated_frequency([+7, +7, -2, -7, -4])
    14
    """
    gen = frequency_generator(freqs)

    s = set()
    freq = 0
    while freq not in s:
        s.add(freq)
        freq = freq + next(gen)
    return freq


if __name__ == '__main__':
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=1)
    frequencies = list(map(int, data.split('\n')))

    a1 = frequency(frequencies)
    print("a1 = %r" % a1)
    aocd.submit1(a1, year=2018, day=1, session=session, reopen=False)

    a2 = find_repeated_frequency(frequencies)
    print("a2 = %r" % a2)
    aocd.submit2(a2, year=2018, day=1, session=session, reopen=False)
