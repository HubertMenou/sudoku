# Sudoku solver

Makes computers solve sudokus for us.

This is a personal project, and as all CS projects, it is not over ;-)

## Where to start

- Solve a sudoku: `python sudoku/demo_direct.py easy_01`
- To solve another sudoku, add a sudoku file in `samples`.

## Sudoku files format

Sudoku files are text files (ending in `.sudoku`)

A sudoku file represent an unfilled sudoku, where the known figures are written naturally, and the unknown figures are denoted by x (lower case). One can use as many blank characters or line jumps to make the sudoku files clearer.

Example:
```
29x 46x 157
841 72x x39
xxx 13x 8xx

6xx xx1 xxx
xxx 2xx x96
x89 xxx 2x5

xxx 9xx 5xx
93x 8x7 xxx
x16 xx2 x7x
```

## Developer notes

To denote *cell* values (1 to 9), use the term *cell values*.
To denote *array* values (0 to 8), use the term *array values*.
`Row index` or `column index` denote a python-like position, with array values.
