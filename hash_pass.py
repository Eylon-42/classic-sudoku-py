import uuid
import hashlib

PASS_LEN = 4


def hash_password(password):
    # uuid is used to generate a random number for more secure password
    salt = uuid.uuid4().hex  # uses later to validate password insert by the user
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    # the uniq value stored in DB is seperated from hash
    # the uniq value and the password entered by user combine in hash and compare
    # to the hash value stored in DB
    password, salt = hashed_password[0].split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
