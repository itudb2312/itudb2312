from flask import Flask, render_template
import mysql.connector as mysql

app = Flask(__name__ )

# Your database configuration
# Create a MySQL connection
db = mysql.connect(
    user='user', 
    password='password', 
    database='mysql',
    host='127.0.0.1', 
    port=3306
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tables')
def tables():
    
    select_query = """SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'mysql';"""
    cursor.execute(select_query)
    result = cursor.fetchall()
    return result

@app.route('/races')
def races():
    select_query = "SELECT * FROM races"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('races.html',races=result)

@app.route('/drivers')
def drivers():
    select_query = "SELECT * FROM drivers"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('drivers.html',drivers=result)

@app.route('/results')
def results():
    
    select_query = "SELECT * FROM results WHERE resultId < 100"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('results.html',results=result)

@app.route('/pit_stops')
def pit_stops():
    select_query = "SELECT * FROM pit_stops"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('pit_stops.html',pit_stops=result)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
