"""
Tic Tac Toe Player
"""

import math
import copy as cp
import random


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
    # Count number of X/0
    num_x = 0
    num_o = 0

    for row in board:
        num_x += row.count(X)
        num_o += row.count(O)

    return O if num_x > num_o else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    i: row of the move (0,1,2)
    j: which cell in the row (column) (0,1,2)

    """
    # Initialize list to store possible actions (i,j)
    possible_actions = []

    # Traverse every row, then col using enumerate() - returns count, value
    for row, value in enumerate(board):
        for col, value in enumerate(board[row]):

            # Use enumerate()'s first return variable to list (row, col)
            if board[row][col] == None:
                possible_actions.append((row, col))

    # Alternatively, repackage enumerate() into another f(x) and use lambda x?

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Deep copy of board
    board_copy = cp.deepcopy(board)

    # an empty action is an invalid action
    if action is not None:
        # Initialize row and col in action set
        row, col = action

        # an action on a filled spot is an invalid action
        if board_copy[row][col] is None:
            board_copy[row][col] = player(board_copy)
        else:
            raise Exception("Invalid action: box is filled")
    else:
        raise Exception("Invalid action: no action input")

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # List winning states (8 of them)
    winning_states = [[(0, 0), (0, 1), (0, 2)],
                      [(1, 0), (1, 1), (1, 2)],
                      [(2, 0), (2, 1), (2, 2)],
                      [(0, 0), (1, 0), (2, 0)],
                      [(0, 1), (1, 1), (2, 1)],
                      [(0, 2), (1, 2), (2, 2)],
                      [(0, 0), (1, 1), (2, 2)],
                      [(0, 2), (1, 1), (2, 0)]]

    # nested for loop to compare winning states
    for win_state in winning_states:
        # initialize list to track possible lines
        line = []

        # find a filled straight line filled with X or Os (3 in a row)
        for x, y in win_state:
            if board[x][y] is not None:
                line.append(board[x][y]) # Winning condition is three in a row of unique character (X or O)

        # return winning symbol if find 3 in a row
        if len(line) == 3 and len(set(line)) == 1:
            # print(line)
            return line[0]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Win (If there is a winner)
    if winner(board) == X or winner(board) == O:
        return True
    # Draw (If all boxes filled out)
    elif not any(None in row for row in board):
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) is None:
        return 0
    elif winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # if game has ended
    if terminal(board):
        return None

    # if AI takes the first turn, randomly choose a box
    if board == initial_state():
        return(random.randint(0,2),random.randint(0,2))

    # initialize list of optimal moves
    optimal_moves = []

    # recursive method for minimax to score and list potential optimal steps
    for action in actions(board):
        if player(board) == O: # If AI is O, they're minimizing
            utility = max_value(result(board, action))
            optimal_moves.append([utility, action])
        elif player(board) == X: # If AI is X, they're maximizing
            utility = min_value(result(board, action))
            optimal_moves.append([utility, action])

    # sorts the list
    optimal_moves.sort()

    # picks the best outcomes
    if player(board) == O:
        # choose (possibly) SMALLEST utility # and returns its associated action
        return optimal_moves[0][1]
    elif player(board) == X:
        # choose (possibly) LARGEST utility # and returns its associated action
        return optimal_moves[-1][1]


def max_value(board):

    # return utility score of terminal board
    if terminal(board):
        return utility(board)

    max_eval = -math.inf
    for action in actions(board):
        max_eval = max(max_eval, min_value(result(board, action)))
    return max_eval

def min_value(board):

    # return utility score of terminal board
    if terminal(board):
        return utility(board)

    min_eval = math.inf
    for action in actions(board):
        min_eval = min(min_eval, max_value(result(board, action)))
    return min_eval
