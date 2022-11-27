
# puzzle = [
#     [4, 3, 5, 2, 6, 9, 7, 8, 1],
#     [6, 8, 2, 5, 7, 1, 4, 9, 3],
#     [1, 9, 7, 8, 3, 4, 5, 6, 2],
#     [8, 2, 6, 1, 9, 5, 3, 4, 7],
#     [3, 7, 4, 6, 8, 2, 9, 1, 5],
#     [9, 5, 1, 7, 4, 3, 6, 2, 8],
#     [5, 1, 9, 3, 2, 6, 8, 7, 4],
#     [2, 4, None, 9, 5, 7, 1, 3, 6],
#     [7, None, 3, 4, 1, 8, 2, 5, 9]
# ]

# puzzle = [
#     [4, 3, 5, 2, 6, 9, 7, 8, 1],
#     [6, 8, 2, 5, 7, 1, 4, 9, 3],
#     [1, 9, 7, 8, 3, 4, 5, 6, 2],
#     [8, 2, 6, 1, 9, 5, 3, 4, 7],
#     [3, 7, 4, 6, 8, 2, 9, 1, 5],
#     [9, 5, 1, 7, 4, 3, 6, 2, 8],
#     [5, 1, 9, 3, 2, 6, 8, 7, 4],
#     [2, 4, 8, 9, 5, 7, 1, 3, 6],
#     [7, 6, 3, 4, 1, 8, 2, 5, 9]
# ]

#
# def consistent(puzzle):
#     x = 0
#     y = 0
#
#     # Check each row for duplicates
#     for row in puzzle:
#         # Keep track of all numbers seen so far
#         observed = set()
#         for value in row:
#             print(f"row: ", value)
#             # If we see a number we've already seen
#             if value in observed and value != None:
#                 return False
#             observed.add(value)
#         print(observed)
#
#     # Check each column for duplicates
#     for col in puzzle:
#         # Keep track of all numbers seen so far
#         observed = set()
#         for value in col:
#             # print(f"col: ", value)
#             # If we see a number we've already seen
#             if value in observed and value != None:
#                 return False
#             observed.add(value)
#     print(observed)
#     # If no constraints violated, then consistent
#     return True
#
#
# def main():
#     print(consistent(puzzle))
#
#

knowledge = And(

)

if __name__ == "__main__":
    main()
