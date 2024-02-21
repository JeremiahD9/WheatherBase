#!/usr/bin/python

from flask import Flask
from flask import render_template, request
import psycopg2
import random
import hashlib
import os
import binascii

app = Flask(__name__)

conn = psycopg2.connect(
    host = "localhost",
    port = "5432",
    database = "kozakw",
    user = "kozakw",
    password = "summer862winter"
)
cur = conn.cursor()

@app.route('/')
def home_page():
    return render_template("login.html", loginText = "")

@app.route('/submit', methods=['POST'])
def login_post():
    user_username = request.form['username']
    user_password = request.form['password']
    
    if request.method == 'POST':
        if 'login' in request.form:
            cur.execute("SELECT password,salt FROM users WHERE login='" + user_username + "';")
            pass_info = cur.fetchone()
            if pass_info is None:
                return render_template("login.html", loginText = "No account found. Please register.")
            else:
                actual_password = pass_info[0]
                salt = pass_info[1]

            if h(user_password, salt.encode()) == actual_password:
                return render_template("valid.html", username = user_username)
            else:
                return render_template("login.html", loginText = "Incorrect password.")

        elif 'register' in request.form:
            cur.execute("SELECT login FROM users WHERE login='" + user_username + "';")
            if cur.fetchone() is not None:
                return render_template("login.html", loginText = "That username is already taken. Try again.")

            if user_username == "" or user_password == "":
                return render_template("login.html", loginText = "Please enter a username and password.")              
            salt = binascii.hexlify(os.urandom(16))
            cur.execute("INSERT INTO users VALUES ('" + user_username + "', '" + h(user_password, salt) + "', '" + salt.decode() + "')")
            conn.commit()
            return render_template("registered.html", username = user_username)

def h(user_password, salt):
    sha256 = hashlib.sha256()
    user_password_bytes = user_password.encode()
    sha256.update(user_password_bytes)
    sha256.update(salt)
    user_password_hash = sha256.hexdigest()
    return user_password_hash

if __name__ == '__main__':
    my_port = 5127
    app.run(host='0.0.0.0', port = my_port) 
