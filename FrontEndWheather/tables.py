from flask import Flask
from flask import render_template
import psycopg2


app = Flask(__name__)

#CHANGE THIS TO JEREMIAH
conn = psycopg2.connect(
    host = "localhost",
    port = "5432",
    database = "dawsonj2",
    user = "dawsonj2",
    password = "eyebrow529redm"
)
cur = conn.cursor()

@app.route('/')
def home_page():
    return render_template("table.html")

if __name__ == '__main__':
    my_port = 5124
    app.run(host='0.0.0.0', port = my_port) 