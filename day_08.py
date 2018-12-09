#!/usr/bin/env python3
# day_08.py
# By Sebastian Raaphorst, 2018.


import aocd


class Node:
    def __init__(self, data_list):
        self.num_children = data_list.pop(0)
        self.metadata_qty = data_list.pop(0)
        self.children = [Node(data_list) for _ in range(self.num_children)]
        self.metadata = [data_list.pop(0) for _ in range(self.metadata_qty)]

    def metadata_serial(self):
        """
        Calculate the serial based on the sum of the metadata across all the nodes in the tree.
        :return: the serial code
        """
        return sum(self.metadata) + sum([c.metadata_serial() for c in self.children])

    def child_metadata_serial(self):
        """
        Calculate the serial in the following way:
        1. If the node has no children, take the sum of the metadata;
        2. Else use the metadata as indices into the children (provided they are legal indices) and take the sums
           of the metadata of those children.
        :return: the serial code
        """
        if self.num_children == 0:
            return sum(self.metadata)
        else:
            return sum([self.children[idx-1].child_metadata_serial() for idx in self.metadata
                       if 1 <= idx <= self.num_children])


def serial_code(immutable_data_list, func):
    """
    Parse a serial number tree and get the serial code it represents from its metadata.
    :param immutable_data_list: the list of numbers representing the tree
    :param func: the method on the node to calculate the metadata
    :return: the metadata sum

    >>> serial_code([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2], func=Node.metadata_serial)
    138
    >>> serial_code([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2], func=Node.child_metadata_serial)
    66
    """

    mutable_data_list = immutable_data_list.copy()
    root = Node(mutable_data_list)
    assert len(mutable_data_list) == 0

    return func(root)


if __name__ == '__main__':
    day = 8
    session = aocd.get_cookie()
    data = aocd.get_data(session=session, year=2018, day=day)
    master_data_list = list(map(int, data.split()))

    a1 = serial_code(master_data_list, func=Node.metadata_serial)

    print('a1 = %r' % a1)
    aocd.submit1(a1, year=2018, day=day, session=session, reopen=False)

    a2 = serial_code(master_data_list, func=Node.child_metadata_serial)
    print('a2 = %r' % a2)
    aocd.submit2(a2, year=2018, day=day, session=session, reopen=False)
