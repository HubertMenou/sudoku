from argparse import ArgumentParser

def get_single_sudoku_file(description=None) -> str:

    parser = ArgumentParser(description=description)

    parser.add_argument("sudoku_file", nargs=1)

    args = parser.parse_args()
    if isinstance(args.sudoku_file, list):
        args.sudoku_file = args.sudoku_file[0]

    sudoku_file = args.sudoku_file
    return sudoku_file
