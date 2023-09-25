import unittest

from sudoku.io_sudoku import IOSudoku
from sudoku.exceptions import \
    SudokuException, \
    UnableToSolveException, \
    InfeasibleSudokuException, \
    MaxIterReachedException, \
    NoChoiceException
from sudoku.choices import SudokuChoices, StaticSudokuChoices

from tests.text_samples import *


class SudokuChoicesTest:

    def __init__(self, choices):
        # Ground truth of the upper-left 3x3 group of boxes
        self.sdk = IOSudoku(EASY_TXT)
        self.known_boxes = ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2))
        self.known_values = (2, 9, 8, 4, 1)
        self.unknown_boxes = ((0, 2), (2, 0), (2, 1), (2, 2))

        self.choices = choices(self.sdk)

    def test_all_final(self):
        self.assertFalse(
            self.choices.all_final(),
            msg="There should exist unknown boxes")

    def test_is_final(self):
        for box in self.known_boxes:
            self.assertTrue(
                self.choices.is_final(box[0], box[1]),
                msg="Box is supposed to be know"
            )

        for box in self.unknown_boxes:
            self.assertFalse(
                self.choices.is_final(box[0], box[1]),
                msg="Box is supposed to be unknow"
            )

        for box, ground_val in zip(self.known_boxes, self.known_values):
            val = self.choices.get_cell_value(box[0], box[1])
            self.assertTrue(val == ground_val)


class TestStaticSudokuChoices(SudokuChoicesTest, unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        SudokuChoicesTest.__init__(self, StaticSudokuChoices)



if __name__ == "__main__":
    unittest.main()
