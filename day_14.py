#!/usr/bin/env python3
# day_14.py
# By Sebastian Raaphorst, 2018.


import aocd


def find_recipes(rounds):
    """
    Calculate the last ten recipes in the sequence.
    :param rounds: the number of rounds
    :return: a list of the last 10 recipes in the sequence

    >>> find_recipes(5)
    [0, 1, 2, 4, 5, 1, 5, 8, 9, 1]
    >>> find_recipes(18)
    [9, 2, 5, 1, 0, 7, 1, 0, 8, 5]
    >>> find_recipes(2018)
    [5, 9, 4, 1, 4, 2, 9, 8, 8, 2]
    """
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    while len(recipes) < rounds + 10:
        new_recipe = recipes[elf1] + recipes[elf2]
        for i in str(new_recipe):
            recipes.append(int(i))
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
    return recipes[rounds:rounds+10]


def find_recipes_2(pattern):
    """
    Calculate the number of recipes in the sequence before the given pattern appears.
    :param pattern: the pattern to identify
    :return: the number of recipes to the left of the pattern

    >>> find_recipes_2('51589')
    9
    >>> find_recipes_2('01245')
    5
    >>> find_recipes_2('92510')
    18
    >>> find_recipes_2('59414')
    2018
    """
    # Make rounds into a list of digits.
    pattern_len = len(pattern)
    digits = [int(i) for i in pattern]
    last_digits = []
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    looking = True
    while looking:
        new_recipe = recipes[elf1] + recipes[elf2]
        for i in str(new_recipe):
            if len(last_digits) == pattern_len:
                last_digits.pop(0)
            recipes.append(int(i))
            last_digits.append(int(i))

            # We have to check here as it could appear in the middle of adding new recipes.
            # In fact, in my case, it does.
            if last_digits == digits:
                looking = False
                break
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
    return len(recipes) - len(digits)


if __name__ == '__main__':
    day = 14
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)
    rounds = int(data)

    a1 = ''.join([str(i) for i in find_recipes(rounds)])
    print('a1 = {}'.format(a1))
    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = find_recipes_2(data)
    print('a2 = %r' % a2)
    aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
