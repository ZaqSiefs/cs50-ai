"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """

    xs = 0
    os = 0
    for row in board:
        for square in row:
            if square == O:
                os += 1
            elif square == X:
                xs += 1
            
    if xs == os:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i, row in enumerate(board):
        for j, square in enumerate(row):
            if square == EMPTY:
                actions.add((i, j))
    
    return actions

def result(board, action):
    if board[action[0]][action[1]] is not EMPTY:
        raise RuntimeError("action can not be committed with current board state")
    
    tempBoard = copy.deepcopy(board)
    tempBoard[action[0]][action[1]] = player(board)

    return tempBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = check_rows(board)
    if winner is not None:
        return winner
    
    winner = check_columns(board)
    if winner is not None:
        return winner
    
    winner = check_diag_tl_br(board)
    if winner is not None:
        return winner
    
    winner = check_diag_tr_bl(board)
    return winner

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    counter = 0
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False

    return True
    
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    theWinner = winner(board)
    if theWinner == X:
        return 1
    elif theWinner == O:
        return -1
    else: 
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    optimal = None

    if player(board) == X:
        maxVal = -math.inf
        for action in actions(board):
            max = optimizeO(result(board, action))
            if max > maxVal:
                maxVal = max
                optimal = action
    else:
        minVal = math.inf
        for action in actions(board):
            min = optimizeX(result(board, action))
            if min < minVal:
                minVal = min
                optimal = action
    return optimal

def optimizeO(board):
    if terminal(board):
        return utility(board)
    
    minVal = math.inf
    for action in actions(board):
        minVal = min(minVal, optimizeX(result(board, action)))

    return minVal

def optimizeX(board):
    if terminal(board):
        return utility(board)
    
    maxVal = -math.inf
    for action in actions(board):
        maxVal = max(maxVal, optimizeO(result(board, action)))
            
    return maxVal

def check_rows(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]
    return None

def check_columns(board):
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] and board[0][column] is not EMPTY:
            return board[0][column]
    return None

def check_diag_tl_br(board):
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    return None

def check_diag_tr_bl(board):
    if board[0][2] == board[1][1] == board[2][0] and board[0][0] is not EMPTY:
        return board[0][2]
    return None