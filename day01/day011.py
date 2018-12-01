#!/usr/bin/env python3


def frequency(freqfile):
    """
    Given a file of frequencies of the form [+-]\d+, with one per line, find their sum.
    :param freqfile: the name of the input file
    :return: the sum of the frequencies
    """
    return sum(map(int, open(freqfile).read().split('\n')))


if __name__ == '__main__':
    print(frequency("input"))
