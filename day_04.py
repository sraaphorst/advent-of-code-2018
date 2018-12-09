#!/usr/bin/env python3
# day_04.py
# By Sebastian Raaphorst, 2018.


import aocd
import re


def parse_schedule(schedule):
    """
    Given a list of sorted scheduling information, produce a list of the guard sleep schedules.
    :param schedule: a list of sorted strings describing scheduling information
    :return: a dictionary from guard ID to array of length 60 indicating how many times the guard slept at that minute

    >>> schedule = []
    >>> schedule.append('[1518-11-01 00:00] Guard #10 begins shift')
    >>> schedule.append('[1518-11-01 00:05] falls asleep')
    >>> schedule.append('[1518-11-01 00:25] wakes up')
    >>> schedule.append('[1518-11-01 00:30] falls asleep')
    >>> schedule.append('[1518-11-01 00:55] wakes up')
    >>> schedule.append('[1518-11-01 23:58] Guard #99 begins shift')
    >>> schedule.append('[1518-11-02 00:40] falls asleep')
    >>> schedule.append('[1518-11-02 00:50] wakes up')
    >>> schedule.append('[1518-11-03 00:05] Guard #10 begins shift')
    >>> schedule.append('[1518-11-03 00:24] falls asleep')
    >>> schedule.append('[1518-11-03 00:29] wakes up')
    >>> schedule.append('[1518-11-04 00:02] Guard #99 begins shift')
    >>> schedule.append('[1518-11-04 00:36] falls asleep')
    >>> schedule.append('[1518-11-04 00:46] wakes up')
    >>> schedule.append('[1518-11-05 00:03] Guard #99 begins shift')
    >>> schedule.append('[1518-11-05 00:45] falls asleep')
    >>> schedule.append('[1518-11-05 00:55] wakes up')
    >>> parse_schedule(schedule)
    {10: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0], 99: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]}
    """
    mutable_schedule = schedule[:]
    date_matcher = re.compile("\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) 00:(?P<minute>\d\d)\].*")
    guard_matcher= re.compile(".*Guard #(?P<guard_id>\d+).*")

    # We want to map a guard to a dict of length 60, which contains the number of minutes a guard slept on a current
    # minute over the entire schedule.
    guard_sleep_schedule = {}

    while len(mutable_schedule) > 0:
        schedule_line = mutable_schedule.pop(0)
        guard_match = guard_matcher.match(schedule_line)
        if guard_match is None:
            raise ValueError('Unexceoect line: "{}"'.format(schedule_line))

        guard = int(guard_match.group('guard_id'))
        guard_sleep_schedule.setdefault(guard, [0] * 60)

        if len(mutable_schedule) == 0:
            break

        # Keep parsing lines until we get another Guard line.
        # If we get a falls asleep line, it must be followed by a
        while len(mutable_schedule) > 0 and 'Guard' not in mutable_schedule[0]:
            # Get the falls asleep line.
            sleep_line = mutable_schedule.pop(0)
            date_match = date_matcher.match(sleep_line)
            if 'asleep' not in sleep_line or date_match is None or len(mutable_schedule) == 0:
                raise ValueError('Unexpected line: {}'.format(sleep_line))
            sleep_start = int(date_match.group('minute'))

            # Get the wakes up line.
            wake_line = mutable_schedule.pop(0)
            date_match = date_matcher.match(wake_line)
            if 'wakes' not in wake_line or date_match is None:
                raise ValueError('Unexpected line: {}'.format(wake_line))
            sleep_end = int(date_match.group('minute'))

            for i in range(sleep_start, sleep_end):
                guard_sleep_schedule[guard][i] += 1

    return guard_sleep_schedule


def find_best_prospect(guard_sleep_schedule):
    """
    Given a guard sleep schedule, which is a dictionary of guard id to lists length 60 showing the number of minutes
    they spent sleeping during the hour starting at midnight, find the sleepiest guard, and the minute he is most
    likely to be asleep.
    :param guard_sleep_schedule: the guard_sleep_schedule
    :return: a pair (guard id, minute)

    >>> schedule = []
    >>> schedule.append('[1518-11-01 00:00] Guard #10 begins shift')
    >>> schedule.append('[1518-11-01 00:05] falls asleep')
    >>> schedule.append('[1518-11-01 00:25] wakes up')
    >>> schedule.append('[1518-11-01 00:30] falls asleep')
    >>> schedule.append('[1518-11-01 00:55] wakes up')
    >>> schedule.append('[1518-11-01 23:58] Guard #99 begins shift')
    >>> schedule.append('[1518-11-02 00:40] falls asleep')
    >>> schedule.append('[1518-11-02 00:50] wakes up')
    >>> schedule.append('[1518-11-03 00:05] Guard #10 begins shift')
    >>> schedule.append('[1518-11-03 00:24] falls asleep')
    >>> schedule.append('[1518-11-03 00:29] wakes up')
    >>> schedule.append('[1518-11-04 00:02] Guard #99 begins shift')
    >>> schedule.append('[1518-11-04 00:36] falls asleep')
    >>> schedule.append('[1518-11-04 00:46] wakes up')
    >>> schedule.append('[1518-11-05 00:03] Guard #99 begins shift')
    >>> schedule.append('[1518-11-05 00:45] falls asleep')
    >>> schedule.append('[1518-11-05 00:55] wakes up')
    >>> find_best_prospect(parse_schedule(schedule))
    (10, 24)
    """
    guard_id = max(guard_sleep_schedule, key=lambda x: sum(guard_sleep_schedule[x]))
    sleep_schedule = guard_sleep_schedule[guard_id]
    minute = max(zip(sleep_schedule, range(60)))[1]
    return guard_id, minute


def find_most_predictable_guard(guard_sleep_schedule):
    """
    Given a guard sleep schedule, which is a dictionary of guard id to lists length 60 showing the number of minutes
    they spent sleeping during the hour starting at midnight, find the guard with the highest number of sleeps for a
    given minute.
    :param guard_sleep_schedule: the guard_sleep_schedule
    :return: a pair(guard id, minute)

    >>> schedule = []
    >>> schedule.append('[1518-11-01 00:00] Guard #10 begins shift')
    >>> schedule.append('[1518-11-01 00:05] falls asleep')
    >>> schedule.append('[1518-11-01 00:25] wakes up')
    >>> schedule.append('[1518-11-01 00:30] falls asleep')
    >>> schedule.append('[1518-11-01 00:55] wakes up')
    >>> schedule.append('[1518-11-01 23:58] Guard #99 begins shift')
    >>> schedule.append('[1518-11-02 00:40] falls asleep')
    >>> schedule.append('[1518-11-02 00:50] wakes up')
    >>> schedule.append('[1518-11-03 00:05] Guard #10 begins shift')
    >>> schedule.append('[1518-11-03 00:24] falls asleep')
    >>> schedule.append('[1518-11-03 00:29] wakes up')
    >>> schedule.append('[1518-11-04 00:02] Guard #99 begins shift')
    >>> schedule.append('[1518-11-04 00:36] falls asleep')
    >>> schedule.append('[1518-11-04 00:46] wakes up')
    >>> schedule.append('[1518-11-05 00:03] Guard #99 begins shift')
    >>> schedule.append('[1518-11-05 00:45] falls asleep')
    >>> schedule.append('[1518-11-05 00:55] wakes up')
    >>> find_most_predictable_guard(parse_schedule(schedule))
    (99, 45)
    """
    # Map the guards to their max sleep minute
    max_sleeps = {guard_id: max(zip(guard_sleep_schedule[guard_id], range(60)))[1] for guard_id in guard_sleep_schedule}
    max_guard = max(max_sleeps, key=lambda x: guard_sleep_schedule[x][max_sleeps[x]])
    return max_guard, max_sleeps[max_guard]


if __name__ == '__main__':
    day = 4
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)
    schedule = parse_schedule(sorted(data.split('\n')))

    a1 = find_best_prospect(schedule)
    a1prod = a1[0] * a1[1]
    print('a1 = %r' % a1prod)
    aocd.submit1(a1prod, year=2018, day=day, session=session, reopen=False)

    a2 = find_most_predictable_guard(schedule)
    a2prod = a2[0] * a2[1]
    print('a2 = %r' % a2prod)
    aocd.submit2(a2prod, year=2018, day=day, session=session, reopen=False)
