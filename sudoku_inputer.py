import queue
import threading

import backtrack as sudoku

max_size = 100
easy_queue = queue.Queue(max_size)
medium_queue = queue.Queue(max_size)
hard_queue = queue.Queue(max_size)


# make board parrallel and put them in queue of 100
# each time a board is taken out from the queue it will fill it again
def make_easy_board(easy):
    # make board after successful solution and than remove 30 numbers
    while True:
        board = sudoku.make_board(3)
        board = sudoku.removeK(3, board)
        easy.put(board)


def make_medium_board(med):
    # make board after successful solution and than remove 40 numbers
    while True:
        board = sudoku.make_board(3)
        board = sudoku.removeK(10, board)
        med.put(board)


def make_hard_board(hard):
    # make board after successful solution and than remove 50 numbers
    while True:
        board = sudoku.make_board(3)
        board = sudoku.removeK(25, board)
        hard.put(board)


def read_board(k):
    # take one board from the right queue according to the
    # difficulty lvl the user has chosen
    if k == 0:
        item = easy_queue.get()
    elif k == 1:
        item = medium_queue.get()
    else:
        item = hard_queue.get()
    return item


def main():
    # start 3 parallels threading to make different lvl sudoku boards
    easy_make = threading.Thread(target=make_easy_board, args=(easy_queue,))
    medium_make = threading.Thread(target=make_medium_board, args=(medium_queue,))
    hard_make = threading.Thread(target=make_hard_board, args=(hard_queue,))
    easy_make.start()
    medium_make.start()
    hard_make.start()


if __name__ == "__main__":
    main()
