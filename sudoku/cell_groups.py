"""Defines box groups for direct solving"""

from typing import Tuple


class Grouping:

    PARENTS = None
    CHILDREN = None

    @classmethod
    def sub_group(cls, parent: Tuple[int]):
        row, col = parent
        pairs = [
            (row + child_row, col + child_col)
            for child_row, child_col in cls.CHILDREN
        ]
        return pairs


class RowGrouping(Grouping):

    PARENTS = tuple([(row, 0) for row in range(9)])
    CHILDREN = tuple([(0, col) for col in range(9)])


class ColumnGrouping(Grouping):

    PARENTS = tuple([(0, col) for col in range(9)])
    CHILDREN = tuple([(row, 0) for row in range(9)])


class BoxGrouping(Grouping):

    PARENTS = tuple([(i, j) for i in [0, 3, 6] for j in [0, 3, 6]])
    CHILDREN = tuple([(i, j) for i in [0, 1, 2] for j in [0, 1, 2]])
