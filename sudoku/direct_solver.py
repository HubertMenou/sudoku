import numpy as np
from typing import Tuple, Type, List

from .choices import SudokuChoices, \
    ForbidOutcome, DirectOutcome, ForceSetOutcome
from .cell_groups import Grouping, RowGrouping, ColumnGrouping, BoxGrouping


class DirectSolver:

    def __init__(self, initial_sudoku: SudokuChoices):
        self.sudoku = initial_sudoku

    def __call__(self) \
            -> Tuple[bool, SudokuChoices]:
        return self.solve()

    def solve(self) -> Tuple[bool, SudokuChoices]:
        """
        Returns:
            - (True, solution) if it was feasible to solve it
              using direct methods,
            - (False, partial_solution) if it was insufficient
              to solve it using direct methods.
        """
        raise NotImplementedError


class EmptyDirectSolver(DirectSolver):

    def solve(self) -> Tuple[bool, SudokuChoices]:
        return False, self.sudoku


class GroupBasedDirectSolver(DirectSolver):

    def solve(self) -> Tuple[bool, SudokuChoices]:
        while True:
            outcome = self.clean_and_isolate()
            if outcome == DirectOutcome.INCONSISTENT_CHANGE:
                return False, self.sudoku
            if outcome == DirectOutcome.NOTHING_CHANGED:
                return self.is_solved(), self.sudoku

    def is_solved(self) -> bool:
        # TODO: determine if it is necessary to check the overall sudoku consistency
        return self.sudoku.all_final()

    def clean_and_isolate(self) -> DirectOutcome:
        cleaning_outcome = self.clean_all_groups()
        if cleaning_outcome == DirectOutcome.INCONSISTENT_CHANGE:
            print("Inconsistent cleaning")
            return DirectOutcome.INCONSISTENT_CHANGE

        # isolation_outcome = DirectOutcome.NOTHING_CHANGED
        isolation_outcome = self.isolate_all_groups()
        if isolation_outcome == DirectOutcome.INCONSISTENT_CHANGE:
            print("Inconsistent isolation")
            return DirectOutcome.INCONSISTENT_CHANGE

        if DirectOutcome.HAS_CHANGED in [cleaning_outcome, isolation_outcome]:
            return DirectOutcome.HAS_CHANGED
        else:
            return DirectOutcome.NOTHING_CHANGED

    def clean_all_groups(self) -> DirectOutcome:
        cleaning_outcome = DirectOutcome.NOTHING_CHANGED
        for group in (RowGrouping, ColumnGrouping, BoxGrouping):
            group_outcome = self.clean_group(group)
            if group_outcome == DirectOutcome.INCONSISTENT_CHANGE:
                return DirectOutcome.INCONSISTENT_CHANGE
            if group_outcome == DirectOutcome.HAS_CHANGED:
                cleaning_outcome = DirectOutcome.HAS_CHANGED
        return cleaning_outcome

    def clean_group(self, group: Type[Grouping]) -> DirectOutcome:
        group_outcome = DirectOutcome.NOTHING_CHANGED
        for parent in group.PARENTS:
            sub_outcome = self.clean_sub_group(group.sub_group(parent))
            if sub_outcome == DirectOutcome.INCONSISTENT_CHANGE:
                return DirectOutcome.INCONSISTENT_CHANGE
            if sub_outcome == DirectOutcome.HAS_CHANGED:
                group_outcome = DirectOutcome.HAS_CHANGED
        return group_outcome

    def clean_sub_group(self, sub_group: List[Tuple[int]]) -> DirectOutcome:
        sub_outcome = DirectOutcome.NOTHING_CHANGED
        final_positions, still_free_positions = list(), list()
        for arr_pos in sub_group:
            if self.sudoku.is_final(arr_pos[0], arr_pos[1]):
                final_positions.append(arr_pos)
            else:
                still_free_positions.append(arr_pos)

        already_used = [
            self.sudoku.get_cell_value(arr_pos[0], arr_pos[1])
            for arr_pos in final_positions
        ]

        for row, col in still_free_positions:
            for cell_value in already_used:
                outcome = self.sudoku.forbid(row, col, cell_value)
                if outcome == ForbidOutcome.LEFT_EMPTY_HANDED:
                    return DirectOutcome.INCONSISTENT_CHANGE
                if outcome == ForbidOutcome.USEFUL:
                    sub_outcome = DirectOutcome.HAS_CHANGED

        return sub_outcome

    def isolate_all_groups(self) -> DirectOutcome:
        isolation_outcome = DirectOutcome.NOTHING_CHANGED
        for group in (RowGrouping, ColumnGrouping, BoxGrouping):
            group_outcome = self.isolate_group(group)
            if group_outcome == DirectOutcome.INCONSISTENT_CHANGE:
                return DirectOutcome.INCONSISTENT_CHANGE
            if group_outcome == DirectOutcome.HAS_CHANGED:
                isolation_outcome = DirectOutcome.HAS_CHANGED
        return isolation_outcome

    def isolate_group(self, group: Type[Grouping]) -> DirectOutcome:
        isolated = False
        for parent in group.PARENTS:
            sub_group = group.sub_group(parent)
            usage = np.zeros((9,), dtype=int)  # cell values
            # location contains inconsistent array indices by default
            location = np.zeros((9, 2), dtype=int)
            for row, col in sub_group:
                choices = self.sudoku.get_cell_value_choices(row, col)
                for cell_value in choices:
                    arr_value = cell_value - 1
                    usage[arr_value] += 1
                    location[arr_value, :] = (row, col)

            for arr_value in range(9):
                row, col = location[arr_value, :]
                if usage[arr_value] != 1 or self.sudoku.is_final(row, col):
                    continue
                cell_value = arr_value + 1
                # print(f"\tIsolating ({row}, {col}) to {cell_value}")
                outcome = self.sudoku.force_set(row, col, cell_value)
                if outcome == ForceSetOutcome.IMPOSSIBLE:
                    return DirectOutcome.INCONSISTENT_CHANGE
                elif outcome == ForceSetOutcome.OK:
                    isolated = True
        return DirectOutcome.HAS_CHANGED if isolated else DirectOutcome.NOTHING_CHANGED
