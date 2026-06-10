import random

class TicTacToe:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def play_move(self, row, col, player):
        self.board[row][col] = player

    def check_winner(self):
        b = self.board

        # Rows
        for row in b:
            if row[0] != "" and row[0] == row[1] == row[2]:
                return row[0]

        # Columns
        for c in range(3):
            if b[0][c] != "" and b[0][c] == b[1][c] == b[2][c]:
                return b[0][c]

        # Diagonals
        if b[0][0] != "" and b[0][0] == b[1][1] == b[2][2]:
            return b[0][0]
        if b[0][2] != "" and b[0][2] == b[1][1] == b[2][0]:
            return b[0][2]

        return None

    def game_result(self, moves):
        for i, (r, c) in enumerate(moves):
            player = "X" if i % 2 == 0 else "O"
            self.play_move(r, c, player)

        winner = self.check_winner()

        if winner == "X":
            return "A"
        if winner == "O":
            return "B"
        if len(moves) == 9:
            return "Draw"
        return "Pending"


def random_game():

    positions = [(r, c) for r in range(3) for c in range(3)]

    random.shuffle(positions)

    game = TicTacToe()
    result = game.game_result(positions)

    return result

print(random_game())
