from flask import Flask, render_template, request
import os
import urllib.parse as up
import psycopg2


app = Flask(__name__)
    
up.uses_netloc.append("postgres")
conn = psycopg2.connect("dbname='zrmfsvop' user='zrmfsvop' host='dumbo.db.elephantsql.com' password='your_password'")
cur = conn.cursor()

@app.route("/")  
def index():  
    return render_template("index.html"); 
 
 
@app.route("/view")  
def view():  
    global cur

    cur.execute("SELECT * FROM Users ORDER BY user_record DESC, user_time ASC")  
    rows = cur.fetchall()  
    conn.commit()
    return render_template("view.html",rows = rows)
 
    
if __name__ == '__main__':
   app.run(debug = True)
