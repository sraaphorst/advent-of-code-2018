#!/usr/bin/env python3
# day_D.py
# By Sebastian Raaphorst, 2018.


import aocd


if __name__ == '__main__':
    day = 0
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)

    a1 = None
    print("a1 = %r" % a1)
    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = None
    print("a2 = %r" % a2)
    aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
