from flask import Flask, render_template, request
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

@app.route('/races', methods=['GET', 'POST'])
def races():
    if request.method == 'POST':
        selected_year = request.form.get('selected_year')

        # Check if the selected year is not empty or "All Years"
        if selected_year and selected_year != "All Years":
            # If a specific year is selected, filter by that year
            select_query = f"SELECT * FROM races WHERE year = {selected_year}"
            cursor.execute(select_query)
            result = cursor.fetchall()
            return render_template('races.html', races=result, selected_year=selected_year)
        else:
            # If no specific year is selected or "All Years," retrieve all races
            select_query = "SELECT * FROM races"
            cursor.execute(select_query)
            result = cursor.fetchall()
            return render_template('races.html', races=result, selected_year="All Years")
    else:
        # Retrieve all races when no specific year is selected
        select_query = "SELECT * FROM races"
        cursor.execute(select_query)
        result = cursor.fetchall()
        return render_template('races.html', races=result)

@app.route('/who_won', methods=['GET'])
def who_won():
    query = "SELECT * FROM races"
    cursor.execute(query)
    races = cursor.fetchall()

    race_data = []
    for race in races:
        winner_name = get_winner(race[0])
        race_data.append({"race_name": race[4], "winner": winner_name})
    return render_template('who_won.html', races=race_data)

def get_winner(race_id):
    query = f'''
        SELECT drivers.forename, drivers.surname
        FROM results
        JOIN drivers ON results.driverId = drivers.driverId
        WHERE results.raceId = {race_id}
        ORDER BY results.points DESC
        LIMIT 1
    '''
    cursor.execute(query)
    winner = cursor.fetchone()

    return f"{winner[0]} {winner[1]}" if winner else "No Winner"
    
@app.route('/drivers', methods=['GET', 'POST'])
def drivers():
    if request.method == 'POST':
        selected_nationality = request.form.get('selected_nationality')
        if selected_nationality and selected_nationality != 'all':
            select_query = f"SELECT * FROM drivers WHERE nationality = '{selected_nationality}'"
        else:
            select_query = "SELECT * FROM drivers"
    else:
        select_query = "SELECT * FROM drivers"

    cursor.execute(select_query)
    result = cursor.fetchall()

    # Retrieve distinct nationalities for the dropdown menu
    cursor.execute("SELECT DISTINCT nationality FROM drivers")
    nationalities = cursor.fetchall()

    return render_template('drivers.html', drivers=result, nationalities=nationalities)

@app.route('/driver_stats')
def driver_stats():
    # Query to get distinct drivers, their winning count, and total points
    query = '''
        SELECT drivers.forename, drivers.surname, SUM(results.points) AS total_points
        FROM drivers
        JOIN results ON drivers.driverId = results.driverId
        GROUP BY drivers.forename, drivers.surname
        ORDER BY total_points DESC;
    '''

    cursor.execute(query)
    driver_stats = cursor.fetchall()

    return render_template('driver_stats.html', driver_stats=driver_stats)

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
    # Query selects circuit informatiom from northern hemisphere, groups them by countries and orders them by their altitudes
    select_query = """
    SELECT name, location, country, alt, url 
    FROM circuits 
    WHERE lat > 0 
    GROUP BY country 
    ORDER BY alt DESC;"""
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('circuits.html',circuits=result)

@app.route('/qualifying')
def qualifying():
    # Query selects driver information by joining the tables, groups them by countries and orders them by their qualifying1 results
    select_query = """
        SELECT drivers.forename, drivers.surname, drivers.nationality
        FROM qualifying
        JOIN drivers ON qualifying.driverId = drivers.driverId
        GROUP BY drivers.nationality
        ORDER BY q1 ASC;
    """
    cursor.execute(select_query)
    result = cursor.fetchall()

    return render_template('qualifying.html',qualifying=result)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
