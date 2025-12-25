def read_sudoku(txt: str) -> list[list[int | None]]:
    sudoku = []
    for line in txt.strip().splitlines():
        row = [
            int(num) if num.isdigit() else None 
            for num in line.strip() 
            if num.isdigit() or num == '.'
        ]
        if len(row) != 9:
            raise ValueError("Each row must contain exactly 9 elements (numbers or '.').")
        sudoku.append(row)
    if len(sudoku) != 9:
        raise ValueError("Sudoku must contain exactly 9 rows.")
    return sudoku


def write_sudoku(sudoku: list[list[int | None]]) -> str:
    return "\n".join(
        "".join(str(num) if num is not None else '.' for num in row)
        for row in sudoku
    )


# Assume that every cell has a set of possible values
# * start eliminating posibilities based on constrained sets
# * row, col, box create different constrainted sets 
# * when a set has only one possibility, assign that value to the cell
# * update the possible values for other cells in the same row, col, box 

# each cell has an id (row, col)
# create the constrained groups (row, col, box)


def get_groups(coord):
    """Return the row, column, and box groups for a given cell coordinate."""
    r, c = coord
    row_group = [(r, col) for col in range(9)]
    col_group = [(row, c) for row in range(9)]
    box_start_row, box_start_col = 3 * (r // 3), 3 * (c // 3)
    box_group = [(row, col) for row in range(box_start_row, box_start_row + 3) 
                             for col in range(box_start_col, box_start_col + 3)]
    return row_group, col_group, box_group

def solve_sudoku(sudoku: list[list[int | None]]) -> list[list[int]]:
    """Solve the given Sudoku puzzle using constraint propagation."""
    # Initialize possible values for each cell
    pb: dict[tuple[int, int], set[int]] = {
        (r, c): set(range(1, 10)) if sudoku[r][c] is None else {sudoku[r][c]}
        for r in range(9) for c in range(9)
    } # possible values

    def _is_solved(sudoku):
        return all(sudoku[r][c] is not None for r in range(9) for c in range(9))
    
    def _are_equal(sudoku1, sudoku2):
        return all(sudoku1[r][c] == sudoku2[r][c] for r in range(9) for c in range(9))

    while not _is_solved(sudoku):
        # make a copy of the current state
        prev_sudoku = [row[:] for row in sudoku]  
        # update the possible values based on current assignments 
        for r in range(9):
            for c in range(9):
                if sudoku[r][c] is None:
                    used_values = set()
                    row_group, col_group, box_group = get_groups((r, c))
                    for group in (row_group, col_group, box_group):
                        for (gr, gc) in group:
                            if sudoku[gr][gc] is not None:
                                used_values.add(sudoku[gr][gc])
                    pb[(r, c)] -= used_values
                    assert len(pb[(r, c)]) > 0, f"No possible values for cell ({r}, {c})"
                    if len(pb[(r, c)]) == 1:
                        sudoku[r][c] = next(iter(pb[(r, c)]))

        # check if any progress was made
        if _are_equal(sudoku, prev_sudoku):
            # breakpoint()
            raise RuntimeError("Stuck: No further progress can be made with the current algorithm (either the puzzle in unsolvable or the algorithm is insufficient).")
        
    return sudoku

if __name__ == "__main__":
    example = """\
2...7.3..
7.3916...
..6.8.15.
..1.94...
...1.....
....2.8..
.62...4.5
.7..5..28
.8...976.
"""
    print("Input Sudoku:")
    print(example.strip().replace(" ", ""))
    sudoku = read_sudoku(example)
    solved_sudoku = solve_sudoku(sudoku)
    print("Solved Sudoku:")
    print(write_sudoku(solved_sudoku))