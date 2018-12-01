#!/usr/bin/env python3


def frequency(freqfile):
    return sum(map(int, open(freqfile).read().split('\n')))


if __name__ == '__main__':
    print(frequency("input"))
