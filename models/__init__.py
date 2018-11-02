from clcrypto import *
from psycopg2 import IntegrityError


class User():

    @staticmethod
    def add(cursor, name, password):
        password = password_hash(password)
        sql = f"INSERT INTO users(username, hashed_password) VALUES('{name}', '{password}');"
        cursor.execute(sql)

    @staticmethod
    def check_pass(cursor, name, password):
        pass_to_check = password_hash(password)
        sql = f"SELECT hashed_password FROM users WHERE username = '{name}';"
        cursor.execute(sql)
        try:
            user_pass = cursor.fetchone()[0]
        except TypeError:
            raise Exception(f"There is no user named '{name}'")


        if user_pass == pass_to_check:
            return True
        else:
            raise Exception("Invalid password")


    @staticmethod
    def user_del(cursor, name, password):
        if User.check_pass(cursor, name, password):
            sql = f"DELETE FROM users WHERE username = '{name}';"
            cursor.execute(sql)

    @staticmethod
    def list(cursor):
        sql = "SELECT id, username, email FROM users"
        cursor.execute(sql)
        user_table = ""
        for row in cursor.fetchall():
            user_table += "ID : " + str(row[0]) + "\n"
            user_table += "Username : " + str(row[1]) + "\n"
            user_table += "Email : " + str(row[2]) + "\n\n"

        return user_table

    @staticmethod
    def edit_password(cursor, name, password, new_password):
        if User.check_pass(cursor, name, password):
            new_password = password_hash(new_password)
            sql = f"UPDATE users SET hashed_password = '{new_password}' WHERE username = '{name}';"
            cursor.execute(sql)

    @staticmethod
    def edit_username(cursor, name, password, new_name):
        if User.check_pass(cursor, name, password):
            try:
                sql = f"UPDATE users SET username = '{new_name}' WHERE username = '{name}';"
                cursor.execute(sql)
            except IntegrityError:
                print(f"'{new_name}' already exist sin base. Username have to be unique.")

    @staticmethod
    def edit_email(cursor, name, password, new_email):
        if User.check_pass(cursor, name, password):
            try:
                sql = f"UPDATE users SET email = '{new_email}' WHERE username = '{name}';"
                cursor.execute(sql)
            except IntegrityError:
                print(f"'{new_email}' already exists in base. Address email have to be unique. ")

    @staticmethod
    def send_message(cursor, name, password, to_who, content):
        if User.check_pass(cursor, name, password) and User.check_user(cursor, to_who):
            sql = f"INSERT INTO messages(from_who, to_who, text) VALUES('{name}', '{to_who}', '{content}');"
            cursor.execute(sql)

    @staticmethod
    def check_user(cursor, name):
        sql = f"SELECT username FROM users WHERE username = '{name}'"
        cursor.execute(sql)
        try:
            user_pass = cursor.fetchone()[0]
            return True
        except TypeError:
            raise Exception(f"There is no user named '{name}'")

    @staticmethod
    def read_all(cursor, name, password):
        if User.check_pass(cursor, name, password):
            sql = f"SELECT to_who, from_who, text, date FROM messages WHERE to_who = '{name}' OR from_who = '{name}';"
            cursor.execute(sql)
            mess_table = "History of your messages:\n\n"
            for row in cursor.fetchall():
                mess_table += "To : " + str(row[0]) + "\n"
                mess_table += "From : " + str(row[1]) + "\n"
                mess_table += "Text : " + str(row[2]) + "\n"
                mess_table += "Send: " + str(row[3]) + "\n\n"

            if mess_table == "History of your messages:\n\n":
                mess_table = "There is no messages"
            print(mess_table)

    @staticmethod
    def read_from(cursor, name, password, from_who):
        if User.check_pass(cursor, name, password) and User.check_user(cursor, from_who):
            sql = f"SELECT to_who, from_who, text, date FROM messages WHERE to_who = '{name}' AND from_who = '{from_who}';"
            cursor.execute(sql)
            mess_table = f"Messages from {from_who}:\n\n"
            for row in cursor.fetchall():
                mess_table += "To : " + str(row[0]) + "\n"
                mess_table += "From : " + str(row[1]) + "\n"
                mess_table += "Text : " + str(row[2]) + "\n"
                mess_table += "Send: " + str(row[3]) + "\n\n"

            if mess_table == f"Messages from {from_who}:\n\n":
                mess_table = "There is no messages"
            print(mess_table)