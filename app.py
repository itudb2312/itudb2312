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

@app.route('/driver_standings')
def driver_standings():
    select_query = """SELECT driver_standings.driverStandingsId, races.name, drivers.surname, 
        driver_standings.points, driver_standings.position, driver_standings.wins
    FROM driver_standings 
    JOIN drivers ON driver_standings.driverId = drivers.driverId
    JOIN races ON driver_standings.raceId = races.raceId
    WHERE drivers.surname = "Hamilton"
    ORDER BY driver_standings.driverStandingsId ASC;
    """
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('driver_standings.html',driver_standings=result)

@app.route('/sprint_results')
def sprint_results():
    select_query = """SELECT sprint_results.resultId, races.name, drivers.surname,
    constructors.name, sprint_results.number, sprint_results.grid, sprint_results.position, sprint_results.points,
    sprint_results.laps, sprint_results.time, sprint_results.milliseconds, sprint_results.fastestLap, sprint_results.fastestLapTime
    FROM sprint_results
    JOIN drivers ON sprint_results.driverId = drivers.driverId
    JOIN races ON sprint_results.raceId = races.raceId
    JOIN constructors ON constructors.constructorId = sprint_results.constructorId
    WHERE drivers.surname = "Hamilton"
    ORDER BY sprint_results.resultId ASC; """

    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('sprint_results.html',sprint_results=result)

@app.route('/circuits')
def circuits():
    select_query = "SELECT * FROM circuits"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('circuits.html',circuits=result)

@app.route('/qualifying')
def qualifying():
    select_query = "SELECT * FROM qualifying"
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('qualifying.html',qualifying=result)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
