from flask import Flask, request
import threading
import sudoku_inputer
import json
import sql_db as DAL
import hash_pass as hash
import backtrack as new_board
import sudoku_inputer as board_maker

app = Flask(__name__)

COOKIE_LST = []


@app.route('/sign_up', methods=['GET', 'POST'])
def new_user():
    with DAL.create_connection('user') as con:
        x = request.get_json()
        user_name = x['username']
        user_password = x['password']
        data = (user_name,)
        # check if the user name exist
        if DAL.check_if_user_exist(con, data):
            # if not exist create hash and create new record in tbale 'user'
            secret = hash.hash_password(user_password)
            data = (user_name, secret)
            DAL.db_write(con, 'user', 'write', data)
            rep = 'register_ok'
        else:
            rep = 'user_exist'
        return rep


@app.route('/login', methods=['POST'])
def login():
    global COOKIE_LST
    with DAL.create_connection('user') as con:
        x = request.get_json()
        user_name = x['username']
        user_password = x['password']
        data = (user_name,)
        # check if user exist
        if not DAL.check_if_user_exist(con, data):
            # read the hash password,from db, of the current user
            rows = DAL.db_read(con, 'user', 'check_pass', data)
            if len(rows) != 0:
                secret = list(rows[0])
                # check if the current password and the hash one match
                if (hash.check_password(secret, user_password)):
                    cookie = hash.hash_password(x['username'])
                    COOKIE_LST.append(cookie)
                    lst = ['\nWelcome  ' + x['username'], cookie]
                    rep = json.dumps(lst)
                    return rep
                else:
                    rep = 'Wrong password'
                return rep
            else:
                return 'No password found'
        else:
            return 'No user found'


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global COOKIE_LST
    x = request.get_json()
    COOKIE_LST.remove(x['hash'])


@app.route('/get_new_sudoku', methods=['GET'])
def get_new_sudoku():
    x = request.get_json()
    if x['hash'] in COOKIE_LST:
        lvl = int(x['difficulty'])
        # Get new board according to the difficuly lvl the user has chosen
        board = board_maker.read_board(lvl)
    rep = json.dumps(board)
    return rep


@app.route('/validate_sudoku', methods=['GET', 'POST'])
def validate_sudoku():
    x = request.get_json()
    # check hash to verify user
    if x['hash'] in COOKIE_LST:
        # if ok validate board solution
        if new_board.validate_sudoku(x['board']):
            data = (x['username'], x['time'], x['difficulty'])
            # if ok write to DB the user name, time and difficulty
            with DAL.create_connection('score') as con:
                DAL.db_write(con, 'score', 'write', data)
                return ('Solution is correct'.encode())
        else:
            return ('Check again'.encode())
    return ('User is not recognize. Try to login'.encode())


@app.route('/ScoreBoard', methods=['GET'])
def get_scoreboard():
    with DAL.create_connection('score') as con:
        x = request.get_json()
        if x['hash'] in COOKIE_LST:
            rows = DAL.db_read_score(con, x['difficulty'])
            rep = json.dumps(rows)
            return rep


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    with DAL.create_connection('score') as con:
        x = request.get_json()
        if x['hash'] in COOKIE_LST:
            rows = DAL.db_read_score(con, 'admin', x['sql'])
            rep = json.dumps(rows)
        return rep


def main():
    make_board = threading.Thread(target=board_maker.main)
    make_board.start()
    flask_run = threading.Thread(target=app.run)
    flask_run.start()


if __name__ == "__main__":
    main()
