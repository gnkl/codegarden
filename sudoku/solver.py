def read_sudoku(txt: str) -> list[list[int | None]]:
    sudoku = []
    for line in txt.strip().splitlines():
        row = [
            int(num) if num.isdigit() else None
            for num in line.strip()
            if num.isdigit() or num == "."
        ]
        if len(row) != 9:
            raise ValueError(
                "Each row must contain exactly 9 elements (numbers or '.')."
            )
        sudoku.append(row)
    if len(sudoku) != 9:
        raise ValueError("Sudoku must contain exactly 9 rows.")
    return sudoku


def write_sudoku(sudoku: list[list[int | None]]) -> str:
    return "\n".join(
        "".join(str(num) if num is not None else "." for num in row) for row in sudoku
    )


# Assume that every cell has a set of possible values
# * start eliminating posibilities based on constrained sets
# * row, col, box create different constrainted sets
# * when a set has only one possibility, assign that value to the cell
# * update the possible values for other cells in the same row, col, box

# each cell has an id (row, col)
# create the constrained groups (row, col, box)


def get_all_groups():
    groups = []
    # rows
    for r in range(9):
        groups.append([(r, c) for c in range(9)])
    # columns
    for c in range(9):
        groups.append([(r, c) for r in range(9)])
    # boxes
    for box_r in range(3):
        for box_c in range(3):
            group = []
            for r in range(box_r * 3, box_r * 3 + 3):
                for c in range(box_c * 3, box_c * 3 + 3):
                    group.append((r, c))
            groups.append(group)
    return groups


def get_groups(coord):
    """Return the row, column, and box groups for a given cell coordinate."""
    r, c = coord
    row_group = [(r, col) for col in range(9)]
    col_group = [(row, c) for row in range(9)]
    box_start_row, box_start_col = 3 * (r // 3), 3 * (c // 3)
    box_group = [
        (row, col)
        for row in range(box_start_row, box_start_row + 3)
        for col in range(box_start_col, box_start_col + 3)
    ]
    return row_group, col_group, box_group


def solve_sudoku(sudoku: list[list[int | None]]) -> list[list[int]]:
    """Solve the given Sudoku puzzle using constraint propagation."""
    # Initialize possible values for each cell
    pb: dict[tuple[int, int], set[int]] = {
        (r, c): set(range(1, 10)) if sudoku[r][c] is None else {sudoku[r][c]}
        for r in range(9)
        for c in range(9)
    }  # possible values

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
                        for gr, gc in group:
                            if sudoku[gr][gc] is not None:
                                used_values.add(sudoku[gr][gc])
                    pb[(r, c)] -= used_values
                    assert (
                        len(pb[(r, c)]) > 0
                    ), f"No possible values for cell ({r}, {c})"
                    if len(pb[(r, c)]) == 1:
                        sudoku[r][c] = next(iter(pb[(r, c)]))

        # check if any progress was made
        if not _are_equal(sudoku, prev_sudoku):
            continue

        # if no progress, try advanced technique
        # check for groups with cells with exact common sets (and remove possiblities from other cells in the group)
        print("Trying constrained set technique...")
        for group in get_all_groups():
            combos = {}
            for r, c in group:
                tup = tuple(
                    sorted(pb[(r, c)])
                )  # transformed version of the set to be hashable
                if tup not in combos:
                    combos[tup] = [(r, c)]
                else:
                    combos[tup].append((r, c))

            for combo, cells in combos.items():
                if len(combo) == len(cells) and len(combo) > 1:
                    # found a constrained set
                    constrained_values = set(combo)
                    for r, c in group:
                        if (r, c) not in cells:
                            pb[(r, c)] -= constrained_values
                            assert (
                                len(pb[(r, c)]) > 0
                            ), f"No possible values for cell ({r}, {c}) after applying constrained set technique."
                            if len(pb[(r, c)]) == 1:
                                sudoku[r][c] = next(iter(pb[(r, c)]))

        if not _are_equal(sudoku, prev_sudoku):
            continue

        # next step would be to implement trial and backtracking
        raise RuntimeError(
            "Stuck: No further progress can be made with the current algorithm (either the puzzle in unsolvable or the algorithm is insufficient)."
        )

    return sudoku


if __name__ == "__main__":
    example = """\
..43...8.
...6....9
.619.....
.2.49....
5.3...9..
....62..3
3....4568
78.....4.
.........
"""
    print("Input Sudoku:")
    print(example.strip().replace(" ", ""))
    sudoku = read_sudoku(example)
    solved_sudoku = solve_sudoku(sudoku)
    print("Solved Sudoku:")
    print(write_sudoku(solved_sudoku))
