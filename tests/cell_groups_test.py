import unittest

from typing import Tuple
from sudoku.cell_groups import Grouping, \
    RowGrouping, \
    ColumnGrouping, \
    BoxGrouping


def check_if_full_partition(grouping):
    """Computes the partition from a grouping,
    and states whether the partition has empty intersection and
    whether the covering of the game grid is complete."""
    sub_groups = list(map(grouping.sub_group, grouping.PARENTS))

    recorded_boxes = list()
    for sub_group in sub_groups:
        for box in sub_group:
            if box in recorded_boxes:
                return False, "found duplicate boxes"
            else:
                recorded_boxes.append(box)
    if len(recorded_boxes) == 81:
        return True, "partition is ok"
    else:
        return False, "partition is missing some boxes"


class TestCellGroups(unittest.TestCase):

    def test_row_grouping(self):
        status, msg = check_if_full_partition(RowGrouping)
        self.assertTrue(status, msg=msg)

    def test_column_grouping(self):
        status, msg = check_if_full_partition(ColumnGrouping)
        self.assertTrue(status, msg=msg)

    def test_box_grouping(self):
        status, msg = check_if_full_partition(BoxGrouping)
        self.assertTrue(status, msg=msg)


if __name__ == "__main__":
    unittest.main()
