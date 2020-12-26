from colorama import Fore
from printy import inputy, printy
from os import system, name
import backtrack

TABLE_STAT = [[''] * 9] * 9
CURSOR_STAT = [0, 0]


class draw_table:
    def __init__(self, board):
        self.draw = None
        self.sign = {0: ' [b]|@', 1: ' [n]|@', 2: ' [n]|@', 3: ' [b]|@', 4: ' [n]|@', 5: ' [n]|@', 6: ' [b]|@',
                     7: ' [n]|@', 8: ' [n]|@'}
        self.numbers = board  # the number's list to insert to the table

    def blue_line(self):
        row = 0
        print(' ', end='')
        for i in range(9):
            print('  ', i, end='')  # help the user to choose the cell coordinate
        print('')
        for i in range(4):
            string = (f'  ' + '[b]+---@' * 9 + '[b]+@')  # the boarders of the table (outline and blocks)
            printy(string)
            if i < 3:
                row = self.seperator(row)  # all the inside boarders

    def seperator(self, row):
        string = ''
        string_2 = (('[b]+@' + ('[n]---+@' * 2) + '[n]---@') * 3 + '[b]+@')
        for x in range(3):
            string += str(row)
            for i in range(9):
                # insert the rigt sign of table alnong with the right number according to the sukoku board
                string += self.sign[i] + ' ' + str(self.numbers[row][i])
            string += ' [b]|@'  # last sign
            row += 1
            printy(string)
            string = ''
            if x < 2:
                printy('  ' + string_2)
        return row
