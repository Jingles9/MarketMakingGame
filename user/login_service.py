import sqlite3
from flask_login import LoginManager


class LoginService():

    def __init__(self):
        self.session_users = []

    def user_exists(self, username):
        connection = sqlite3.connect('db/users.db')
        cursor = connection.cursor()
        sql_command = """ SELECT username FROM users;"""
        cursor.execute(sql_command)
        existing_usernames = cursor.fetchall()
        connection.close()
        for existing_username in existing_usernames:
            if username == existing_username[0]:
                return True
        return False

    def login_session_user(self, user):
        self.session_users.append(user)

    def logout_session_user(self, user):
        self.session_users.remove(user)

    def check(self, username, password):
        connection = sqlite3.connect('db/users.db')
        cursor = connection.cursor()
        sql_command = """ SELECT username FROM users;"""
        cursor.execute(sql_command)
        usernames = cursor.fetchall()

        sql_command = """ SELECT password FROM users;"""
        cursor.execute(sql_command)
        passwords = cursor.fetchall()

        connection.close()

        # Note the length of usernames will be the same as passwords, ie: the number of users
        for (user_name, pass_word) in zip(usernames, passwords):
            if username == user_name and password == pass_word:
                return True
        return False

    def new_user(self, username, password):
        connection = sqlite3.connect('db/users.db')
        cursor = connection.cursor()
        sql = """ INSERT INTO users VALUES ("{}", "{}");"""
        query = sql.format(str(username), password)
        cursor.execute(query)
        connection.commit()
        connection.close()

    def get_user(self, username):
        for user in self.session_users:
            if (user.username == username):
                return user
        return None
