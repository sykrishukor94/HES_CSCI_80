import pygame
import sys
import time

# import tictactoe as ttt

# Test for initial_state

# user = None
# board = ttt.initial_state()
# ai_turn = False

# source = (input("Choose X or O: "))
# if source == "X":
#     user = ttt.X
#     ai = ttt.O
# elif source == "O":
#     user = ttt.O
#     ai = ttt.X
#
# # test for minimax()
#
#
# # Test for player()
# print(ttt.player(board))
#
# print(board)
#
# board[0][2] = ai
#
# print(board)
#
# board[1][1] = user
# print(board)
#
# # Test for actions()
# print(ttt.actions(board))
#
#
# # Test for result(board, action)
# board = ttt.result(board, (1,0))
#
# print(ttt.player(board))
#
# board = ttt.result(board, (2,2))
# print(board)
#
# # Test for actions()
# print(ttt.actions(board))
#
# print(ttt.player(board))


board = [["X", "O", "O"],
         ["X", "O", "X"],
         ["O", "X", None]]
#
#         # [["X", "O", "O"],
#         # [None, "O", None],
#         # ["X", "X", "O"]]
#
# print(ttt.actions(board))
# print(board)
# print(ttt.winner(board))
# print(ttt.terminal(board))

opt = []


optimal = [(0,(1,2)),(0,(1,0)),(0,(0,0)),(0,(0,0))]

print(optimal)
optimal.sort()

print(optimal)

#
#
# board = [["X", "O", "O"],
#          ["X", "O", "X"],
#          ["X", "X", "O"]]
#
# winner = ttt.winner(board)
# print(ttt.terminal(board))
#
# if winner is None:
#     print(f"Game Over: Tie.")
# else:
#     print(f"Game Over: {winner} wins.")

# while True:
#
#     game_over = ttt.terminal(board)
#     player = ttt.player(board)
#
#     if game_over:
#         winner = ttt.winner(board)
#         if winner is None:
#             title = f"Game Over: Tie."
#         else:
#             title = f"Game Over: {winner} wins."
#     elif user == player:
#         title = f"Play as {user}"
#     else:
#         title = f"Computer thinking..."
#
#     # Check for AI move
#     if user != player and not game_over:
#         if ai_turn:
#             time.sleep(0.5)
#             move = ttt.minimax(board)
#             board = ttt.result(board, move)
#             ai_turn = False
#         else:
#             ai_turn = True