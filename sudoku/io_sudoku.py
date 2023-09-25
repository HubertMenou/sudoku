"""For file interfacing"""
import os
import numpy as np
from typing import Union
from io import StringIO


SUDOKU_SAMPLES_DIRECTORY = "samples"
EMPTY_CHARACTER = 'x'
ALLOWED_CHARACTERS = f'123456789{EMPTY_CHARACTER}'


class IOSudoku:

    EMPTY_CELL = 0
    EMPTY_CELL_STR = str(EMPTY_CELL)

    def __init__(self, file: Union[str, np.ndarray] = None):
        """Input-Output operations for sudokus

        Different possibilities for the input file:
            - If ``file`` is a single-line str, then it conveys
              the file name of a sudoku in the sample folder,
            - If ``file`` is a multi-line str, then it conveys
              the sudoku itself,
            - If ``file`` is None, then the IOSudoku is left empty.

        :@param file: Loads a sudoku from the file object
        """
        self.grid = np.ones((9, 9), dtype=int) * self.EMPTY_CELL

        if file is None:
            return

        if isinstance(file, str):
            if len(file.splitlines()) == 1:
                self.load_from_file(file)
            else:
                self.load_from_txt(file)
        elif isinstance(file, np.ndarray):
            self.grid = file
        else:
            raise ValueError("Inconsistent input sudoku!")

    def load_from_file(self, file: str):
        """Loads from a file located in the sample directory"""

        if not file.endswith(".sudoku"):
            file += ".sudoku"

        path_to_file = os.path.join(
            SUDOKU_SAMPLES_DIRECTORY, file)

        with open(path_to_file, "r") as reader:
            txt = reader.read()

        self.load_from_txt(txt)

    def load_from_txt(self, txt: str):
        """Loads from a str directly describing the sudoku"""
        txt = txt.splitlines()

        counter = 0
        for idx, line in enumerate(txt):
            if self._digest_txt_line(counter, line):
                counter += 1

            if counter >= 9:
                break

    def _digest_txt_line(self, row: int, line: str) -> bool:
        if line.strip() == '':
            return False

        raw_characters = line.replace(" ", '')
        characters = [c for c in line if c in ALLOWED_CHARACTERS]

        if len(raw_characters) != len(characters):
            raise RuntimeError(f"There are invalid characters: {line}")

        if len(characters) != 9:
            return RuntimeError("Invalid number of character")

        for col, ch in enumerate(characters):
            value = self.EMPTY_CELL if ch == EMPTY_CHARACTER else int(ch)
            self.set_cell(row, col, value)

        return True

    def set_cell(self, row: int, col: int, value: int):
        self.grid[row, col] = value

    def get_cell(self, row: int, col: int) -> int:
        return self.grid[row, col]

    def __str__(self):
        txt = StringIO()
        for row in range(9):
            for col in [0, 3, 6]:
                three_cells = map(str, self.grid[row, col:col + 3])
                txt.write(" ".join(three_cells))
                txt.write("  ")
            txt.write('\n')
            if row in [2, 5]:
                txt.write('\n')
        txt = txt.getvalue()
        return txt.replace(self.EMPTY_CELL_STR, '.')
