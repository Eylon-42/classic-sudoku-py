import sqlite3
from sqlite3 import Error

''' One database with 2 tables 'user' and 'score'
    user - user and password
    score - name , time in minutes , difficulty
    the sql command will be choose from the 2  dictionary above
'''

user = {'path': r"sudoku_db01.db",
        'write': '''insert into user VALUES(?,?)''',
        'update': '''update user set password = ? where user=?''',
        'check_pass': '''select password from user where user=? ''',
        'read': "select * from user"}

score = {'path': r"sudoku_db01.db",
         'write': '''insert into score VALUES(?,?,?) ''',
         'read': "SELECT TOP 10 * FROM score ORDER BY time DESC"}


def create_connection(table_name):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        if table_name == 'user':
            conn = sqlite3.connect(user['path'])
        elif table_name == 'score':
            conn = sqlite3.connect(score['path'])
        return conn
    except Error as e:
        print(e)
    return conn


def db_write(conn, table_name, command_type, data=''):
    try:

        c = conn.cursor()
        if table_name == 'user':
            if command_type == 'write':
                sql = (user['write'])
            else:
                sql = (user['update'])
        else:
            sql = (score['write'])
        c.execute(sql, data)
        conn.commit()
        return True
    except Error as e:
        err = str(e)
        # not necessary because we take care of this problem from the login menu
        if 'UNIQUE constraint' in err:
            print('User ''{}'' is taken. Try again'.format(data[0]))
        else:
            print(e)
        return False


def db_read(conn, table_name, command_type, data):
    try:
        c = conn.cursor()
        if table_name == 'user':
            sql = (user['check_pass'])
        else:
            sql = (score['read'])
        c.execute(sql, data)

        rows = c.fetchall()
        return rows
    except Error as e:
        print(e)


def check_if_user_exist(conn, data):
    c = conn.cursor()
    sql = 'select user from user where user=?'
    c.execute(sql, data)
    row = c.fetchone()
    if row == data:
        return False
    else:
        return True


def db_read_score(conn, data='',
                  sql="select * from score where difficulty=? order by time asc limit 10"):
    c = conn.cursor()
    # if admin the sql request will be given by this user
    if data == 'admin':
        c.execute(sql)
    else:
        data = (data,)
        c.execute(sql, data)
    rows = c.fetchall()
    return rows
