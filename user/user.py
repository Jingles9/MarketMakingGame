from flask_login import UserMixin
import sqlite3

BUY = 'buy'
SELL = 'sell'

class User(UserMixin):

    def __init__(self, username):
        self.username = username
        self.position = 0
        self.trades = []
        self.bid = None
        self.ask = None
        
    def update_password(self, new_pass):
        connection = sqlite3.connect('db/users.db')
        cursor = connection.cursor()
        sql_command = """ UPDATE users SET password = "{}" WHERE username = "{}";"""
        sql_query = sql_command.format(str(new_pass), str(self.username))
        cursor.execute(sql_query)
        connection.close()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return self.username
        
    def remove_order(self, side):
        if side == BUY:
            self.bid = None
        if side == SELL:
            self.ask = None

    def place_order(self, side, value):
        if side == BUY:
            self.bid = value
        if side == SELL:
            self.ask = value

    def fill_order(self, side):
        if side == BUY:
            self.execute_trade(BUY, self.bid)
            self.remove_order(BUY)
        if side == SELL:
            self.execute_trade(SELL, self.ask)
            self.remove_order(SELL)

    def execute_trade(self, side, value):
        if side == BUY:
            self.position += 1
        if side == SELL:
            self.position -= 1
        self.trades.append((side, value))

    def get_pnl(self):
        pnl = 0
        for (side, value) in self.trades:
            print(side)
            print(value)
            if side == BUY:
                pnl -= value
            if side == SELL:
                pnl += value
        return pnl
