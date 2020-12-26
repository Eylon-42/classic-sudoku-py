import json
import requests
import datetime
from draw_table import draw_table

USER_DATA = {'username': '', 'hash': '', 'difficulty': '', 'time': 0, 'board': []}
difficulty_lst = ['Easy', 'Medium', 'Hard']
start_time = ''


def login_signup():
    # uses to login users or signup new users
    global USER_DATA
    ans = input('\nWelcom to sudoku fun game\nPlease Choose:\n1 - To login\n2 - To Signup\n')
    if ans != '1' and ans != '2':
        print('Someting went worng\nMake sure you type the right choice\n')
    else:
        pass_check = ''
        while pass_check != 'pass_ok':
            # loop to keep asking password in case of wrong one
            username = input('Enter user name: ')
            password = input('Enter password: ')
            # login for exist user
            if ans == '1':
                pass_check = requests.post('http://127.0.0.1:5000/login',
                                           json={'username': username, 'password': password})
                if username not in pass_check.content.decode():
                    # if no user found
                    print(pass_check.content.decode())
                else:
                    # if user exist save uniq hash
                    rep = json.loads(pass_check.content)
                    USER_DATA['username'] = username
                    USER_DATA['hash'] = (rep[1])
                    pass_check = 'pass_ok'
                    print(rep[0])
            # sign up for new user
            elif ans == '2':
                rep = requests.post('http://127.0.0.1:5000/sign_up', json={'username': username, 'password': password})
                if rep.content.decode() == 'register_ok':
                    # the process succseed.
                    # the user need to login with the new user name ans password
                    print('Account created\nPlease login with your user name and password')
                    ans = '1'
                else:  # the user is taken. try again
                    print('User is taken choose another one')


def main_menu(ans):
    global start_time
    if ans == '1':  # Get new board game
        board_type = int(input('Choose board difficulty\n0 - Easy\n1 - Meduim\n2 - Hard\n'))
        USER_DATA['difficulty'] = difficulty_lst[board_type]
        rep = requests.get('http://127.0.0.1:5000/get_new_sudoku',
                           json={'hash': USER_DATA['hash'], 'difficulty': board_type})
        new_board = json.loads(rep.content)
        USER_DATA['board'] = new_board
        # once the users reciev board the clock is tiking
        start_time = datetime.datetime.now().replace(microsecond=0)
        print_board()  # print sudoku in table
    elif ans == '2':  # Get the 10 most fastest players for each lvl
        print('ScoreBoard for the 10 most fastest players\n')
        print('username |\ttime in minutes |\tdifficulty\n')
        for i in range(len(difficulty_lst)):  # print all 3 lvl's
            rep = requests.get('http://127.0.0.1:5000/ScoreBoard',
                               json={'hash': USER_DATA['hash'], 'difficulty': difficulty_lst[i]})
            rows = json.loads(rep.content.decode())
            for row in rows:
                print(row[0] + '\t\t      ' + row[1] + '\t\t   ' + row[2])
                print('____________________________________________\n')
        return ''
    elif ans == '3':  # Logout
        rep = requests.get('http://127.0.0.1:5000/logout',
                           json={'hash': USER_DATA['hash']})
        return 'finish'


def print_board():
    board = USER_DATA['board']
    while True:
        draw = draw_table(board)
        draw.blue_line()
        ans = player_move()
        if ans == 'send':
            send_board()
            break
        elif ans == 'exit':
            break


def player_move():
    input_lst = ''
    print("\nEnter 3 numbers separated by space\n")
    print("The first number = Y coordinate, The second number = X coordinate, The third number = your number\n")
    while len(input_lst) != 3:
        input_lst = input(
            'Cell place [x,y] and number [1-9]  OR\nType \'exit\' to main menu  OR\nType \'send\' to check finished sudoku\n').split()
        # if the user want to finish the game or get new board
        if ('exit' in input_lst) or ('send' in input_lst):
            return input_lst[0]
        else:
            # Insert cell coordinate and guessed number (with spaces between)
            if len(input_lst) == 3:
                x = int(input_lst[0])  # X coordinate
                y = int(input_lst[1])  # Y coordinate
                num = int(input_lst[2])  # number to insert
                # insert number into cell only if it is empty
                if USER_DATA['board'][x][y] == ' ':
                    USER_DATA['board'][x][y] = num


def send_board():
    global start_time
    stop_time = datetime.datetime.now().replace(microsecond=0)
    USER_DATA['time'] = str(stop_time - start_time)
    rep = requests.post('http://127.0.0.1:5000/validate_sudoku',
                        json={'username': USER_DATA['username'], 'hash': USER_DATA['hash'],
                              'time': USER_DATA['time'], 'difficulty': USER_DATA['difficulty'],
                              'board': USER_DATA['board']})

    if (rep.content.decode()) == 'Check again':
        print('\n      ' + rep.content.decode() + '\n')
        print_board()
    else:
        print(rep.content.decode())


def admin_query():
    ans = input('Type query from sql or finish:\n')
    if ans != 'finish':
        rep = requests.get('http://127.0.0.1:5000/admin',
                           json={'hash': USER_DATA['hash'], 'sql': ans})
        rows = json.loads(rep.content.decode())
        for row in rows:
            print(row)


if __name__ == "__main__":
    login_signup()
    choice = ''
    while choice != 'finish':
        if USER_DATA['username'] == 'admin':  # user admin only
            admin_query()
        else:  # other users
            ans = input('\nPlease choose:\n1 - Get new sudoku board\n2 - Get ScoreBoard\n3 - Logout\n')
            if 1 <= int(ans) <= 3:
                choice = main_menu(ans)
