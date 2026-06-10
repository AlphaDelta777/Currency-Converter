import pytest
from Tic_Tac_Toe_winner_Judge import TicTacToe, random_game

def test_A_wins():
    game = TicTacToe()
    moves = [[0,0],[1,0],[0,1],[1,1],[0,2]] 
    assert game.game_result(moves) == "A"

def test_B_wins():
    game = TicTacToe()
    moves = [
        [0,0], [0,2],
        [1,0], [1,1],
        [2,2], [2,0]
    ]
    assert game.game_result(moves) == "B"


def test_draw():
    game = TicTacToe()
    moves = [
        [0,0],[0,1],[0,2],
        [1,1],[1,0],[1,2],
        [2,1],[2,0],[2,2]
    ]
    assert game.game_result(moves) == "Draw"

def test_random_game_valid_result():
    result = random_game()
    assert result in ["A", "B", "Draw"]
