class SudokuValidator:
    def __init__(self):
        """Initializes the validator."""
        pass

    def is_valid_board(self, board: list[list[str]]) -> bool:
        """
        Determines if a 9x9 Sudoku board is valid.
        Only filled cells are validated.
        """
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for r in range(9):
            for c in range(9):
                val = board[r][c]

                if val == ".":
                    continue

                # Formula to map grid coordinates to one of the nine 3x3 boxes
                box_idx = (r // 3) * 3 + (c // 3)

                # If the value is already tracked in this row, column, or box, it's invalid
                if val in rows[r] or val in cols[c] or val in boxes[box_idx]:
                    return False

                # Track the value
                rows[r].add(val)
                cols[c].add(val)
                boxes[box_idx].add(val)

        return True


validator = SudokuValidator()

# Instantiate the validator class
validator = SudokuValidator()


board_1 = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

print(f"Example 1 Output: {validator.is_valid_board(board_1)}")

board_2 = [
    ["8", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

print(f"Example 2 Output: {validator.is_valid_board(board_2)}")
