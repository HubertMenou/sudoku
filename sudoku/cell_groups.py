"""Defines box groups for direct solving"""

from typing import Tuple


class Grouping:
    """
    In this context:
        - A group is a set of boxes which should not
        contain the same value twice.
        - A parent is one of the box coordinates within a group.
        - The children are the difference of coordinates describing a group,
        with respect to a given parent coordinate.
        - A grouping is a set of groups described as parents/children.

    The parents are described in ARRAY values.

    See the associated example in the RowGrouping docstring.
    """

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
    """
    One group is one row.
    The parents are the first boxes on the left.

    Example
    -------

    +===+===+===+===+===+===+===+===+===+
    $ A | B | C $ D | E | F $ G | H | J $
    +---+---+---+---+---+---+---+---+---+
    $   |   |   $   |   |   $   |   |   $
    +---+---+---+---+---+---+---+---+---+
    $   |   |   $   |   |   $   |   |   $
    +===+===+===+===+===+===+===+===+===+
    $   |   |   $   |   |   $   |   |   $
    +---+---+---+---+---+---+---+---+---+
    $   |   |   $   |   |   $   |   |   $
    +---+---+---+---+---+---+---+---+---+
    $   |   |   $   |   |   $   |   |   $
    +===+===+===+===+===+===+===+===+===+
    $   |   |   $   |   |   $   |   |   $
    +---+---+---+---+---+---+---+---+---+
    $   |   |   $   |   |   $   |   |   $
    +---+---+---+---+---+---+---+---+---+
    $   |   |   $   |   |   $   |   |   $
    +===+===+===+===+===+===+===+===+===+

    The boxes A-B-C-D-E-F-G-H-J belong to the same group.
    Their parent is A. Described with respect to A, the children
    description of the group is simply:
        ((0, 0), (0, 1), ..., (0, 8), (0, 9))
    """

    PARENTS = tuple([(row, 0) for row in range(9)])
    CHILDREN = tuple([(0, col) for col in range(9)])


class ColumnGrouping(Grouping):
    """
    One group is one column.
    The parents are the first boxes on the top.
    """

    PARENTS = tuple([(0, col) for col in range(9)])
    CHILDREN = tuple([(row, 0) for row in range(9)])


class BoxGrouping(Grouping):
    """
    One group is one of the basic 3x3 boxes.
    The parents are the upper-left boxes.
    """

    PARENTS = tuple([(i, j) for i in [0, 3, 6] for j in [0, 3, 6]])
    CHILDREN = tuple([(i, j) for i in [0, 1, 2] for j in [0, 1, 2]])
