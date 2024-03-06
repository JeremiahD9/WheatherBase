from flask import Flask
from flask import render_template
import psycopg2


app = Flask(__name__)

#CHANGE THIS T O JEREMIAH
conn = psycopg2.connect(
    host = "localhost",
    port = "5432",
    database = "dawsonj2",
    user = "dawsonj2",
    password = "eyebrow529redm"
)
cur = conn.cursor()

def get_name_options():
    
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dawsonj2",
        user="dawsonj2",
        password="eyebrow529redm")
    
    cur = conn.cursor()

    query = "SELECT * FROM complete_table;"
    cur.execute(query)
    
    rows = cur.fetchall()
    

    html = ""
    for row in rows:
        html = html + "<tr>"

        for r in row:
            temp = r
            html = html + f"<td>{temp}</td>"


        #Here is more info on Python's Formatted Strings
        #    https://docs.python.org/3/tutorial/inputoutput.html
        html = html + "</tr>"

        #Backslash n in a string means New Line
        
    
    return html

@app.route('/')
def home_page():
    html_string = get_name_options()

    return render_template("table.html", DropdownOptions = html_string)

if __name__ == '__main__':
    my_port = 5124
    app.run(host='0.0.0.0', port = my_port) 
    


#        html = html + f'<tr><td>"{country}</td><td>{location_name}</td><td>{latitude}</td><td>{longitude}</td><td>{timezone}</td>"</tr>'
