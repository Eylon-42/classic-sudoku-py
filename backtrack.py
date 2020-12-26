import random


def validate_sudoku(board, c=0):
    m = 3
    c = 0
    validate = False
    # check all 81 numbers
    while c < 81:
        i, j = divmod(c, 9)  # the current cell coordinate
        i0, j0 = i - i % m, j - j % m  # the start position of the 3 x 3  block
        current_number = board[i][j]  # current number to check
        board[i][j] = '0'  # take the number out of lst in order to check if we find duplicates

        if (current_number not in board[i]  # not in row
                and all(row[j] != current_number for row in board)  # not in column
                and all(current_number not in row[j0:j0 + m]  # not in block
                        for row in board[i0:i0 + m])):
            board[i][j] = current_number  # if duplicate not found return the number to its place for next check
            validate = True
        else:
            return False  # we found duplicate. solution not good
        c += 1
        if c + 1 >= 81 and validate:  # finish all numbers in table and did not found duplicate
            return validate


def make_board(m=3):
    """Return a random filled m**2 x m**2 Sudoku board."""
    n = m ** 2
    board = [[0 for _ in range(n)] for _ in range(n)]

    def search(c=0):
        "Recursively search for a solution starting at position c."
        i, j = divmod(c, n)
        i0, j0 = i - i % m, j - j % m  # Origin of mxm block
        numbers = list(range(1, n + 1))
        random.shuffle(numbers)
        for x in numbers:
            if (x not in board[i]  # not in row
                    and all(row[j] != x for row in board)  # not in column
                    and all(x not in row[j0:j0 + m]  # not in block
                            for row in board[i0:i])):
                board[i][j] = x
                # if not end of board and did not found duplicate call function recursively
                if c + 1 >= n ** 2 or search(c + 1):
                    return board  # end of board and found solution (meaning no duplicates)
        else:
            # No number is valid in this cell: backtrack and try again.
            board[i][j] = 0
            return None

    return search()


def removeK(K, board):
    count = int(K)
    client_board = board
    while count != 0:
        cellID = random.randint(0, 80)  # pick random cell number
        i = cellID // 9  # get the x coordinate
        j = cellID % 9  # get the y coordinate
        if j != 0:
            j = j - 1
        if client_board[i][j] != 0:  # if there is a number in the cell
            count -= 1  # counter according to the difficulty lvl
            client_board[i][j] = ' '  # delete number
    return client_board
