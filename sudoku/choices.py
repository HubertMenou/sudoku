
import numpy as np
from typing import Type, List
from enum import Enum
from io import StringIO

from .io_sudoku import IOSudoku
from .exceptions import \
    SudokuException, \
    UnableToSolveException, \
    InfeasibleSudokuException, \
    MaxIterReachedException, \
    NoChoiceException


class ForbidOutcome(Enum):

    LEFT_EMPTY_HANDED = 0 # Forbade the last possible choice
    USEFUL = 1  # Forbade a choice that was available, and leaves at least one choice
    USELESS = 2 # Forbade a choice that was already forbidden


class DirectOutcome(Enum):

    INCONSISTENT_CHANGE = 0  # An inconsistent operation occured
    HAS_CHANGED = 1  # Something changed (consistently)
    NOTHING_CHANGED = 2  # Nothing changed


class ForceSetOutcome(Enum):

    IMPOSSIBLE = 0
    OK = 1
    USELESS = 2


class SudokuChoices:

    def __init__(self):
        pass

    def __str__(self):
        raise NotImplementedError

    def to_IOSudoku(self) -> IOSudoku:
        raise NotImplementedError

    def forbid(self, arr_row: int, arr_col: int, cell_value: int) -> ForbidOutcome:
        """Removes the current value from the possible choices,
        the outcome specifies what precisely happened"""
        raise NotImplementedError

    def force_set(self, arr_row: int, arr_col: int, cell_value: int) -> ForceSetOutcome:
        """Forces designated cell to equal cell value"""
        raise NotImplementedError

    def is_final(self, arr_row: int, arr_col: int) -> bool:
        """Says whether the designated cell has its final value,
        ie that there is only one possible choice"""
        raise NotImplementedError

    def get_cell_value(self, arr_row: int, arr_col: int) -> int:
        """Returns the value of the designated cell,
        but does NOT check is there is only one value available
        """
        raise NotImplementedError

    def number_of_choices(self, arr_row: int, arr_col: int) -> int:
        """Counts the number of possible choices in the designated cell"""
        raise NotImplementedError

    def get_cell_value_choices(self, arr_row: int, arr_col: int) -> List[int]:
        """Returns a list of possible cell value choices"""
        raise NotImplementedError

    def all_final(self) -> bool:
        """Says whether all the cells have there final value"""
        raise NotImplementedError



class StaticSudokuChoices(SudokuChoices):

    def __init__(self, sudoku: IOSudoku):
        """

        (choice)_ij: list = [list of possible values]


        (choice)_ij = [v0, v1, v2, v3, v4, v5, v6, v7, v8]
                      |------------------|---------------|
                         Allowed values   Forbidden values
        Number of allowed values: (count)_ij
        """
        super().__init__()
        self._choices = np.zeros((9, 9, 9), dtype=int)
        self._count = np.zeros((9, 9), dtype=int)

        for row in range(9):
            for col in range(9):
                cell_value = sudoku.get_cell(row, col)
                if cell_value == IOSudoku.EMPTY_CELL:
                    self._choices[row, col, :] = np.arange(1, 10)
                    self._count[row, col] = 9
                else:
                    self._choices[row, col, 0] = cell_value
                    self._count[row, col] = 1

    def __str__(self):
        txt = StringIO()
        for row in range(9):
            for col in [0, 3, 6]:
                counts = self._count[row, col:col + 3]
                choices = self._choices[row, col:col + 3, 0]
                three_cells = [f'[{counts[k]}]' if counts[k] > 1 else f' {choices[k]} ' for k in range(3)]
                txt.write(" ".join(map(str, three_cells)))
                txt.write("  ")
            txt.write('\n')
            if row in [2, 5]:
                txt.write('\n')
        return txt.getvalue()

    def show_details(self):
        col2size = [
            max([self.number_of_choices(row, col) for row in range(9)])
            for col in range(9)
        ]
        txt = StringIO()
        for row in range(9):
            for col in range(9):
                size = col2size[col]
                if self.number_of_choices(row, col) == 1:
                    t = str(self.get_cell_value(row, col))
                else:
                    t = "".join(map(str, self.get_cell_value_choices(row, col)))
                txt.write((size - len(t)) * " " + t)
                txt.write("  ")
            txt.write('\n')
            if row in [2, 5]:
                txt.write('\n')
        print(txt.getvalue())

    def to_IOSudoku(self) -> IOSudoku:
        return IOSudoku(self._choices[:, :, 0])

    def forbid(self, arr_row: int, arr_col: int, cell_value: int) -> ForbidOutcome:
        """Removes the current value from the possible choices,
        the outcome specifies what precisely happened"""
        count_ij = self._count[arr_row, arr_col]
        choices = self._choices[arr_row, arr_col, :count_ij]

        if count_ij == 1:
            if cell_value == choices[0]:
                return ForbidOutcome.LEFT_EMPTY_HANDED
            else:
                return ForbidOutcome.USELESS

        if count_ij == 0:
            raise ValueError(f"(count)_({arr_row},{arr_col}) is already 0")

        if cell_value not in choices:
            return ForbidOutcome.USELESS

        new_choices = [c for c in choices if c != cell_value]
        self._choices[arr_row, arr_col, :count_ij - 1] = new_choices
        self._choices[arr_row, arr_col, count_ij - 1] = 0
        self._count[arr_row, arr_col] -= 1

        return ForbidOutcome.USEFUL

    def force_set(self, arr_row: int, arr_col: int, cell_value: int) -> ForceSetOutcome:
        """Forces designated cell to equal cell value"""
        if cell_value not in self.get_cell_value_choices(arr_row, arr_col):
            return ForceSetOutcome.IMPOSSIBLE

        count = self.number_of_choices(arr_row, arr_col)
        if count == 1:
            return ForceSetOutcome.USELESS

        self._choices[arr_row, arr_col, 0] = cell_value
        self._choices[arr_row, arr_col, 1:count] = 0
        self._count[arr_row, arr_col] = 1

        return ForceSetOutcome.OK


    def is_final(self, arr_row: int, arr_col: int) -> bool:
        """Says whether the designated cell has its final value,
        ie that there is only one possible choice"""
        return self._count[arr_row, arr_col] == 1

    def get_cell_value(self, arr_row: int, arr_col: int) -> int:
        """Returns the value of the designated cell,
        but does NOT check is there is only one value available
        """
        return self._choices[arr_row, arr_col, 0]

    def number_of_choices(self, arr_row: int, arr_col: int) -> int:
        """Counts the number of possible choices in the designated cell"""
        return self._count[arr_row, arr_col]

    def get_cell_value_choices(self, arr_row: int, arr_col: int) -> List[int]:
        """Returns a list of possible cell value choices"""
        nb = self._count[arr_row, arr_col]
        return list(self._choices[arr_row, arr_col, :nb])

    def all_final(self) -> bool:
        """Says whether all the cells have there final value"""
        return np.all(self._count == 1)
