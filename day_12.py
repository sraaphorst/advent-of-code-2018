#!/usr/bin/env python3
# day_12.py
# By Sebastian Raaphorst, 2018.
#
# This one could be substantially cleaned up, but I really hated this problem of a stable but constantly right-shifting
# 1D cellular automaton.


import aocd
from bitarray import bitarray


def bitarray_to_int(bit_array):
    """
    Transform a bitarray into an int.
    :param bit_array:
    :return:
    """
    return int(bit_array.to01(), 2)


class Pots:
    """
    This is strikingly similar to a 2D model of Conway's Game of Life.
    Every generation can add two plants to the right, and two to the left.
    Thus if we start with n plants and g generations, our array of plants will be of size:
       n + 2g + 2g = n + 4g
    We take advantage of Python's negative indexing to put the pots on the left of 0 at the end of the array.
    """
    def __init__(self, data):
        # Process the raw data
        lines = [l.strip().replace('.', '0').replace('#', '1') for l in data.split('\n') if l.strip() != '']

        # Process the initial state, which is 15 chars into the first line.
        self.initial_state = bitarray(lines.pop(0)[15:])
        self._transitions = {bitarray_to_int(bitarray(line[0:5])): int(line[-1]) for line in lines}

    @staticmethod
    def _evaluate_state(state, zero_pot_idx):
        return sum([i - zero_pot_idx for i, j in enumerate(state) if j])

    def run_simulation(self, generations=20):
        """
        Run the simulation to determine the sum of the pots containing plants after the given number of generations.
        :param generations: the numebr of generations
        :return: the sum of the pots with plants

        >>> init_data = '''initial state: #..#.#..##......###...###\\n\\n...## => #\\n..#.. => #\\n.#... => #\\n.#.#. => #\\n.#.## => #\\n.##.. => #\\n.#### => #\\n#.#.# => #\\n#.### => #\\n##.#. => #\\n##.## => #\\n###.. => #\\n###.# => #\\n####. => #\\n'''
        >>> p = Pots(init_data)
        >>> p.run_simulation(500)
        325
        """
        # Start at the first position after the empty left pots.
        state = self.initial_state[:]

        # We will reach a state of stability where the string keeps moving right.
        zero_pot_idx = 0
        cyclic_generation = 0
        cyclic_diff = 0

        for generation in range(generations):
            prev_state_string = state.to01().strip('0')

            # We need the state to have five empty pots on the left and five empty pots on the right.
            state_string = state.to01()
            # print('{}: {}'.format(generation, state_string.replace('0', '.').replace('1', '#')))
            if state_string[:5].find('1') == -1:
                left_zeros_to_add = 0
            else:
                left_zeros_to_add = 5 - state_string[:5].index('1')
            if state_string[-5:].find('1') == -1:
                right_zeros_to_add = 0
            else:
                right_zeros_to_add = 5 - state_string[-5:][::-1].index('1')

            # For processing simplicity, make state the same length as newstate.
            state = bitarray('0' * left_zeros_to_add) + state[:] + bitarray('0' * right_zeros_to_add)
            newstate = state[:]

            # The zero pot has migrated right by left_zeros_to_add
            zero_pot_idx += left_zeros_to_add

            for x in range(2, len(newstate) - 2):
                # Grab the slice from the current state and find it in the transitions to set the state
                # at position x.
                substate = state[x-2:x+3]

                lookup = bitarray_to_int(substate)
                if lookup not in self._transitions:
                    newstate[x] = 0
                else:
                    newstate[x] = self._transitions[bitarray_to_int(substate)]

            # Determine if we have reached cyclic stability.
            state_string = newstate.to01().strip('0')
            if prev_state_string == state_string:
                cyclic_generation = generation
                cyclic_diff = Pots._evaluate_state(newstate, zero_pot_idx) - Pots._evaluate_state(state, zero_pot_idx)
                break

            # Otherwise, continue with the next state.
            state = newstate

        # If we found a cycle, very generation after cyclic_generation adds a fixed amount by shifting the pots to the
        # right.
        prefix = 0
        if cyclic_diff != 0:
            prefix = cyclic_diff * (generations - cyclic_generation)

        # Now sum the pots containing plants.
        return prefix + sum([i - zero_pot_idx for i, j in enumerate(state) if j])


if __name__ == '__main__':
    day = 12
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)

    # 2917
    a1 = Pots(data).run_simulation()
    print('a1 = %r' % a1)
    #aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    # 3250000000956
    a2 = Pots(data).run_simulation(50000000000)
    print('a2 = %r' % a2)
    #aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
