from flask import Flask
from flask import request, redirect, url_for, flash
from flask import render_template
import random
import psycopg2

app = Flask(__name__)
app.secret_key = '19021999'

def isUserInDB(Username, Password):
    
    conn = None
    try:

        conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="leen2",
        user="leen2",
        password="chip574pencil")
        
        cur = conn.cursor()

        sql="""
        SELECT username, password FROM userInfo 
        WHERE username = %s  AND password = %s"""
        
        cur.execute(sql,[Username, Password],
        )

        row = cur.fetchone()

        if(row is not None):
            print(row)
            return Username  
        else:
            print("nothing")
            return None

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



@app.route('/')
def welcome():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/submit-login', methods=['POST'])
def submit_login():
    username = request.form['username']
    password = request.form['password']
    user = isUserInDB(username, password)
    if user:
        return render_template("welcome.html", userName=username)
    else:
        flash('Login Failed. Please check your username and password.')
        print("it didnt work idot")
        return render_template("index.html")
        
if __name__ == '__main__':
    my_port = 5128
    app.run(host='0.0.0.0', port = my_port) 

