#!/usr/bin/env python3


def frequency_generator(freqfile):
    """
    Given a file of frequencies, i.e. a line-separated list of numbers of the form [+-]\d+, stream
    them infinitely.
    :param freqfile: the name of the file containing the frequencies
    :return: the next frequency
    """
    freqs = list(map(int, open(freqfile).read().split('\n')))
    n = 0
    while True:
        if n == len(freqs):
            n = 0
        yield freqs[n]
        n = n + 1


def find_repeated_freq(freqfile):
    """
    For a list of frequencies that affect the current state, find the first repeating frequency.
    :param freqfile:
    :return: the first repeated frequency
    """
    gen = frequency_generator(freqfile)

    s = set()
    freq = 0
    while freq not in s:
        s.add(freq)
        freq = freq + next(gen)
    return freq


if __name__ == '__main__':
    print(find_repeated_freq("input"))
