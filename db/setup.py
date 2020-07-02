import sqlite3
import requests
from os import path
import json


def bootstrap_db():
    bootstrap_users_db()
    # populate_users_db()


def bootstrap_users_db():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    sql_command = """ CREATE TABLE users (username VARCHAR(50), password VARCHAR(100));"""
    cursor.execute(sql_command)
    connection.commit()
    connection.close()


def populate_users_db():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    sql = """ INSERT INTO users (name, password) VALUES ("{}", "{}");"""
    query = sql.format('jack', 'jack')
    cursor.execute(query)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    bootstrap_db()
