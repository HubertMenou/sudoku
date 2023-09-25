
from sudoku.direct_solver import GroupBasedDirectSolver
from sudoku.io_sudoku import IOSudoku
from sudoku.choices import SudokuChoices, StaticSudokuChoices
from sudoku.parsers import get_single_sudoku_file


def demo_groupe_based_solver(sudoku_file: str):
    sudoku = IOSudoku(sudoku_file)
    choices = StaticSudokuChoices(sudoku)
    print(choices)

    d_solver = GroupBasedDirectSolver(choices)

    d_solver.solve()
    print(choices.to_IOSudoku())



if __name__ == "__main__":
    sudoku_file = get_single_sudoku_file()
    demo_groupe_based_solver(sudoku_file)
