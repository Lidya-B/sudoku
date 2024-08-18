# ****************************************************************************************************
#
# File name:   sudoku.py
# Description:
#       This program generates random sudoku and uses backtracking to solve it
#
# ****************************************************************************************************

import random


# ****************************************************************************************************

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("-" * 21)

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            if j == 8:
                print(board[i][j] if board[i][j] != 0 else ".")
            else:
                print(board[i][j] if board[i][j] != 0 else ".", end=" ")


# ****************************************************************************************************

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j  # row, col
    return None


# ****************************************************************************************************

def valid(board, num, pos):
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


# ****************************************************************************************************

def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


# ****************************************************************************************************

def fill_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                num_list = list(range(1, 10))
                random.shuffle(num_list)
                for num in num_list:
                    if valid(board, num, (i, j)):
                        board[i][j] = num
                        if fill_board(board):
                            return True
                        board[i][j] = 0
                return False
    return True


# ****************************************************************************************************

def remove_numbers(board, num_holes=40):
    count = 0
    while count < num_holes:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            backup = board[row][col]
            board[row][col] = 0

            board_copy = [row[:] for row in board]
            if not solve(board_copy):
                board[row][col] = backup
            else:
                count += 1


# ****************************************************************************************************

def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    fill_board(board)
    while True:
        remove_numbers(board)
        board_copy = [row[:] for row in board]
        if solve(board_copy):
            break
        else:
            board = [[0] * 9 for _ in range(9)]
            fill_board(board)
    return board


# ****************************************************************************************************

def main():
    board = generate_sudoku()
    print("Solve this Sudoku puzzle:")
    print_board(board)

    while True:
        action = input("Type 'solve' to solve the puzzle,"
                       " 'quit' to exit, or enter your move as 'row col num'. All numbers must be 1-9: ")
        if action == 'solve':
            if solve(board):
                print("Solved Sudoku puzzle:")
                print_board(board)
            else:
                print("No solution exists for this puzzle.")
            break
        elif action == 'quit':
            print("Exiting...")
            break
        else:
            try:
                row, col, num = map(int, action.split())
                if row < 1 or row > 9 or col < 1 or col > 9 or num < 1 or num > 9:
                    print("Invalid input. Row, column, and number must be between 1 and 9.")
                    continue
                if board[row - 1][col - 1] != 0:
                    print("Cell is full. Try a different cell.")
                    continue
                if valid(board, num, (row - 1, col - 1)):
                    board[row - 1][col - 1] = num
                    print_board(board)
                else:
                    print("Wrong number. Try again.")
            except ValueError:
                print("Invalid input. Please enter your move as 'row col num'.")


# ****************************************************************************************************

if __name__ == "__main__":
    main()
