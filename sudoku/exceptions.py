"""Sudoku-specific exceptions"""

class SudokuException(Exception):
    pass


class UnableToSolveException(SudokuException):
    """Raised whenever a step is blocking when solving a sudoku"""
    pass

class InfeasibleSudokuException(UnableToSolveException):
    """Raised when a sudoku is declared infeasible"""
    pass

class MaxIterReachedException(UnableToSolveException):
    pass

class NoChoiceException(UnableToSolveException):
    pass
