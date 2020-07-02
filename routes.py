from flask import render_template, request, redirect, url_for, Response, flash
import flask_login
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from server import app, login_service, exchange
from user.user import User
import requests

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('book'))
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        if login_service.check(username, passwd):
            user = User(username)
            login_service.login_session_user(user)
            login_user(user)
            return redirect(url_for('exchange'))
        else:
            return Response(status="401")
    return render_template('login.html')

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('book'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if (login_service.user_exists(username)):
            return Response(status="401")
        else:
            login_service.new_user(username, password)
            user = User(username)
            login_service.login_session_user(user)
            login_user(user)
            return redirect(url_for('book'))
    return render_template('signup.html')

@app.route('/exchange.html', methods=['GET', 'POST'])
@login_required
def book():
    if request.method == 'POST':
        bid = request.form['bid']
        offer = request.form['offer']
        bid = None if bid == "" else int(bid)
        ask = None if offer == "" else int(offer)
        exchange.process_passive(current_user, bid=bid, ask=ask)
    return render_template('exchange.html', table=exchange.get_table())
