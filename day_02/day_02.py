#!/usr/bin/env python3
# day_02.py
# By Sebastian Raaphorst, 2018.


import aocd


def calculate_package_checksum(packages):
    """
    Given  a list of packages, calculate its checksum, which is the number of words with two repeated letters times
    the number of words with three letters.
    :param packages: list of package names
    :return: the checksum as specified above

    >>> calculate_package_checksum(['abcdef', 'bababc', 'abbcde', 'abcccd' 'aabcdd', 'abcdee', 'ababab'])
    12
    """

    twocount, threecount = 0, 0
    for package in packages:
        # Make a map according to num letters.
        letters = {}
        for letter in package:
            letters.setdefault(letter, 0)
            letters[letter] += 1

        twocount += 1 if 2 in letters.values() else 0
        threecount += 1 if 3 in letters.values() else 0

    return twocount * threecount


def find_close_packages(packages):
    """
    Given a list of packages, find the two packages who have all but one letter in common in a position
    :param packages: list of packages
    :return: the common letters

    >>> find_close_packages(['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz'])
    'fgij'
    """

    for p1, p2 in [(packages[i], packages[j]) for i in range(len(packages)) for j in range(i, len(packages))]:
        common_letters = [p[0] for p in zip(p1, p2) if p[0] == p[1]]
        if len(common_letters) == len(p1) - 1:
            return ''.join(common_letters)

    return None


if __name__ == '__main__':
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=2)
    package_list = data.split('\n')

    a1 = calculate_package_checksum(package_list)
    print("a1 = %r" % a1)
    aocd.submit1(a1, year=2018, day=2, session=session, reopen=False)

    a2 = find_close_packages(package_list)
    print("a2 = %r" % a2)
    aocd.submit2(a2, year=2018, day=2, session=session, reopen=False)
