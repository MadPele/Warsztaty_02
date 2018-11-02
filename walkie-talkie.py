from psycopg2 import connect
import argparse
from models import User

# -*- coding: utf-8 -*-


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', nargs=1)
    parser.add_argument('-p', '--password', nargs=1)
    parser.add_argument('-ep', '--edit_password', nargs=1)
    parser.add_argument('-eu', '--edit_username', nargs=1)
    parser.add_argument('-t', '--to', nargs=1)
    parser.add_argument('-m', '--message', nargs=1)
    parser.add_argument('-ee', '--edit_email', nargs=1)
    parser.add_argument('-rf', '--read_from', nargs=1)
    parser.add_argument('-a', '--add_user', action="store_true")
    parser.add_argument('-l', '--list', action="store_true")
    parser.add_argument('-ra', '--read_all', action="store_true")
    parser.add_argument('-d', '--delete_user', action="store_true")
    return parser.parse_args()

def user_operations(args):
    cnx = connect(user='postgres',
                  password='coderslab',
                  host='localhost',
                  database="relship")

    cnx.autocommit = True
    cursor = cnx.cursor()

    if args.username and args.password and args.edit_password:
        User.edit_password(cursor, args.username[0], args.password[0], args.edit_password[0])

    if args.username and args.password and args.edit_username:
        User.edit_username(cursor, args.username[0], args.password[0], args.edit_username[0])

    if args.username and args.password and args.edit_email:
        User.edit_email(cursor, args.username[0], args.password[0], args.edit_email[0])

    if args.username and args.password and args.add_user:
        User.add(cursor, args.username[0], args.password[0])

    if args.username and args.password and args.delete_user:
        User.user_del(cursor, args.username[0], args.password[0])

    if args.username and args.password and args.to and args.message:
        User.send_message(cursor, args.username[0], args.password[0], args.to[0], args.message[0])

    if args.username and args.password and args.read_all:
        User.read_all(cursor, args.username[0], args.password[0])

    if args.username and args.password and args.read_from:
        User.read_from(cursor, args.username[0], args.password[0], args.read_from[0])

    if args.list:
        user_table = User.list(cursor)
        print(user_table)

    cursor.close()
    cnx.close()



def Main():
    args = arg_parser()
    user_operations(args)





if __name__ == '__main__':
    Main()


"""


"""

"""
    if args.username and args.password and not args.edit and not args.delete and not args.send and not args.list:
        try:
            create_user(args.username[0], args.password[0])

    if args.username and args.password :
        us.user = check_user(args.username[0])
        if args.new_pass:
            if checked(user.hashed_password):
                salt = generate_salt()
                user.set_password(args.new_pass[0], salt)
                user.save_to_db(cursor)
            else:
                print("Podaj prawidlowe haslo!")
        else:
            print("Podaj nowe haslo w parametrze -n!")
"""