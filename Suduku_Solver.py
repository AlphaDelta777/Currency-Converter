class SudokuSolver:
    """
    A class used to solve a 9x9 Sudoku puzzle grid.
    """

    def solve_sudoku(self, board: list[list[str]]) -> None:
        """
        Solves the Sudoku puzzle in-place using backtracking.

        Args:
            board (list[list[str]]): A 2D list representing the 9x9 Sudoku grid.
        """
        self._backtrack(board)

    def _is_valid(self, board: list[list[str]], row: int, col: int, char: str) -> bool:
        """
        Checks if placing a character at board[row][col] is valid.
        """
        for i in range(9):
            if board[row][i] == char:
                return False
            if board[i][col] == char:
                return False
            box_row = 3 * (row // 3) + i // 3
            box_col = 3 * (col // 3) + i % 3
            if board[box_row][box_col] == char:
                return False
        return True

    def _backtrack(self, board: list[list[str]]) -> bool:
        """
        Helper method that performs the recursive backtracking search.
        """
        for r_idx in range(9):
            for c_idx in range(9):
                if board[r_idx][c_idx] == '.':
                    for num in range(1, 10):
                        char = str(num)
                        if self._is_valid(board, r_idx, c_idx, char):
                            board[r_idx][c_idx] = char

                            if self._backtrack(board):
                                return True

                            board[r_idx][c_idx] = '.'

                    return False
        return True


def print_board(board: list[list[str]]) -> None:
    """Helper function to print the Sudoku board cleanly."""
    for row in board:
        print(" ".join(row))


if __name__ == "__main__":
    
    puzzle = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]

    print("--- UNFINISHED SUDOKU ---")
    print_board(puzzle)
    
    solver = SudokuSolver()
    solver.solve_sudoku(puzzle)
    
    print("\n--- SOLVED SUDOKU ---")
    print_board(puzzle)